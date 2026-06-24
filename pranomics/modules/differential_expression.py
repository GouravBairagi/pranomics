import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class DifferentialExpressionConfig:
    counts: str = "counts/gene_count_matrix.csv"
    metadata: str = "metadata.csv"
    outdir: str = "DEG"
    sample_col: str = "sample"
    condition_col: str = "condition"
    control: str | None = None
    treatment: str | None = None
    fdr: float = 0.05
    logfc: float = 1.0
    min_count: int = 10
    min_samples: int = 2
    overwrite: bool = False


def _read_table(path):
    sep = "\t" if str(path).lower().endswith((".tsv", ".txt")) else ","
    return pd.read_csv(path, sep=sep)


def _load_counts(path):
    df = _read_table(path)
    if df.empty or df.shape[1] < 2:
        raise ValueError("Count matrix must contain a gene column and at least one sample column.")

    gene_col = df.columns[0]
    df = df.rename(columns={gene_col: "gene_id"})
    df["gene_id"] = df["gene_id"].astype(str)

    sample_cols = [col for col in df.columns if col != "gene_id"]
    for col in sample_cols:
        df[col] = pd.to_numeric(df[col], errors="raise")

    if df["gene_id"].duplicated().any():
        raise ValueError("Count matrix contains duplicate gene IDs in the first column.")

    return df.set_index("gene_id")


def _load_metadata(path, sample_col, condition_col):
    metadata = _read_table(path)
    required = {sample_col, condition_col}
    missing = required.difference(metadata.columns)
    if missing:
        raise ValueError(
            f"Metadata is missing required column(s): {', '.join(sorted(missing))}"
        )

    metadata = metadata.copy()
    metadata[sample_col] = metadata[sample_col].astype(str)
    metadata[condition_col] = metadata[condition_col].astype(str)

    if metadata[sample_col].duplicated().any():
        raise ValueError(f"Metadata column '{sample_col}' contains duplicate sample names.")

    return metadata


def _select_contrast(metadata, condition_col, control, treatment):
    conditions = list(pd.unique(metadata[condition_col]))

    if control is None or treatment is None:
        if len(conditions) != 2:
            raise ValueError(
                "Please provide --control and --treatment when metadata has more than two conditions."
            )
        control = conditions[0] if control is None else control
        treatment = conditions[1] if treatment is None else treatment

    missing = [value for value in (control, treatment) if value not in conditions]
    if missing:
        raise ValueError(
            f"Condition value(s) not found in metadata: {', '.join(missing)}"
        )

    return control, treatment


def _align_inputs(counts, metadata, sample_col, condition_col, control, treatment):
    metadata = metadata[metadata[condition_col].isin([control, treatment])].copy()
    metadata_samples = list(metadata[sample_col])
    count_samples = list(counts.columns)

    missing_in_counts = [sample for sample in metadata_samples if sample not in count_samples]
    if missing_in_counts:
        raise ValueError(
            "Metadata sample(s) missing from count matrix: "
            + ", ".join(missing_in_counts)
        )

    usable_samples = [sample for sample in metadata_samples if sample in count_samples]
    counts = counts[usable_samples]
    metadata = metadata.set_index(sample_col).loc[usable_samples].reset_index()

    group_sizes = metadata[condition_col].value_counts()
    too_small = group_sizes[group_sizes < 2]
    if not too_small.empty:
        print(
            "Warning: at least one condition has fewer than two replicates; "
            "statistical power will be limited."
        )

    return counts, metadata


def _edgeR_script():
    return r'''
args <- commandArgs(trailingOnly=TRUE)
counts_file <- args[[1]]
metadata <- args[[2]]
sample_col <- args[[3]]
condition_col <- args[[4]]
control <- args[[5]]
treatment <- args[[6]]
out_results <- args[[7]]
out_norm <- args[[8]]
min_count <- as.numeric(args[[9]])
min_samples <- as.numeric(args[[10]])

suppressPackageStartupMessages({
  library(edgeR)
})

counts <- read.csv(counts_file, row.names=1, check.names=FALSE)
metadata <- read.csv(metadata, check.names=FALSE)
metadata[[sample_col]] <- as.character(metadata[[sample_col]])
metadata[[condition_col]] <- as.character(metadata[[condition_col]])

metadata <- metadata[metadata[[condition_col]] %in% c(control, treatment), , drop=FALSE]
counts <- counts[, metadata[[sample_col]], drop=FALSE]

group <- factor(metadata[[condition_col]], levels=c(control, treatment))
y <- DGEList(counts=counts, group=group)

keep <- rowSums(cpm(y) > min_count) >= min_samples
if (sum(keep) == 0) {
  stop("No genes passed filtering. Lower --min-count or --min-samples.")
}

y <- y[keep, , keep.lib.sizes=FALSE]
y <- calcNormFactors(y)
design <- model.matrix(~ group)
y <- estimateDisp(y, design)
fit <- glmQLFit(y, design)
qlf <- glmQLFTest(fit, coef=2)

results <- topTags(qlf, n=Inf)$table
results$gene_id <- rownames(results)
results <- results[, c("gene_id", setdiff(colnames(results), "gene_id"))]
write.csv(results, out_results, row.names=FALSE)

norm <- cpm(y, normalized.lib.sizes=TRUE, log=FALSE)
norm <- data.frame(gene_id=rownames(norm), norm, check.names=FALSE)
write.csv(norm, out_norm, row.names=FALSE)
'''


def _write_deg_outputs(results_file, outdir, fdr, logfc):
    df = pd.read_csv(results_file)
    if "gene_id" not in df.columns:
        first = df.columns[0]
        df = df.rename(columns={first: "gene_id"})

    df["FDR"] = df["FDR"].fillna(1.0)
    up = df[(df["FDR"] < fdr) & (df["logFC"] > logfc)]
    down = df[(df["FDR"] < fdr) & (df["logFC"] < -logfc)]

    outdir = Path(outdir)
    up.to_csv(outdir / "upregulated.csv", index=False)
    down.to_csv(outdir / "downregulated.csv", index=False)

    summary = outdir / "summary.txt"
    with summary.open("w", encoding="utf-8") as handle:
        handle.write("=== Differential Expression Summary ===\n\n")
        handle.write(f"Total genes tested: {len(df)}\n")
        handle.write(f"FDR cutoff: {fdr}\n")
        handle.write(f"Absolute logFC cutoff: {logfc}\n")
        handle.write(f"Upregulated genes: {len(up)}\n")
        handle.write(f"Downregulated genes: {len(down)}\n")

    return {
        "results": str(results_file),
        "upregulated": str(outdir / "upregulated.csv"),
        "downregulated": str(outdir / "downregulated.csv"),
        "summary": str(summary),
    }


def run_differential_expression(config=None, **kwargs):
    if config is None:
        config = DifferentialExpressionConfig(**kwargs)
    elif kwargs:
        raise ValueError("Pass either a config object or keyword arguments, not both.")

    if shutil.which("Rscript") is None:
        raise RuntimeError("Rscript was not found. Install R and the edgeR Bioconductor package.")

    outdir = Path(config.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    results_file = outdir / "DE_results.csv"
    norm_file = outdir / "normalized_cpm.csv"

    if results_file.exists() and not config.overwrite:
        print(f"Differential expression already exists: {results_file}")
        return _write_deg_outputs(results_file, outdir, config.fdr, config.logfc)

    counts = _load_counts(config.counts)
    metadata = _load_metadata(config.metadata, config.sample_col, config.condition_col)
    control, treatment = _select_contrast(
        metadata, config.condition_col, config.control, config.treatment
    )
    counts, metadata = _align_inputs(
        counts,
        metadata,
        config.sample_col,
        config.condition_col,
        control,
        treatment,
    )

    prepared_counts = outdir / "prepared_counts.csv"
    prepared_metadata = outdir / "prepared_metadata.csv"
    counts.to_csv(prepared_counts)
    metadata.to_csv(prepared_metadata, index=False)

    with tempfile.NamedTemporaryFile("w", suffix=".R", delete=False, encoding="utf-8") as script:
        script.write(_edgeR_script())
        script_path = script.name

    cmd = [
        "Rscript",
        "--vanilla",
        script_path,
        str(prepared_counts),
        str(prepared_metadata),
        config.sample_col,
        config.condition_col,
        control,
        treatment,
        str(results_file),
        str(norm_file),
        str(config.min_count),
        str(config.min_samples),
    ]

    print(f"Running edgeR contrast: {treatment} vs {control}")
    try:
        subprocess.run(cmd, check=True)
    finally:
        try:
            os.remove(script_path)
        except OSError:
            pass

    outputs = _write_deg_outputs(results_file, outdir, config.fdr, config.logfc)
    outputs["normalized_cpm"] = str(norm_file)
    print(f"Differential expression complete: {results_file}")
    return outputs


def run_edger():
    return run_differential_expression()
