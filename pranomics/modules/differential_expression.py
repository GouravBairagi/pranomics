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


# -----------------------------
# SAFE DEG POST-PROCESSING
# -----------------------------
def _standardize_results(df: pd.DataFrame) -> pd.DataFrame:

    # gene column safety
    if "gene_id" not in df.columns:
        df = df.rename(columns={df.columns[0]: "gene_id"})

    # FDR fallback
    if "FDR" not in df.columns:
        if "padj" in df.columns:
            df["FDR"] = df["padj"]
        else:
            df["FDR"] = 1.0

    # logFC fallback
    if "logFC" not in df.columns:
        if "log2FoldChange" in df.columns:
            df["logFC"] = df["log2FoldChange"]
        else:
            df["logFC"] = 0.0

    df["FDR"] = df["FDR"].fillna(1.0)
    df["logFC"] = df["logFC"].fillna(0.0)

    return df


# -----------------------------
# OUTPUT WRITER
# -----------------------------
def _write_deg_outputs(results_file, outdir, fdr, logfc):

    df = pd.read_csv(results_file)
    df = _standardize_results(df)

    up = df[(df["FDR"] < fdr) & (df["logFC"] > logfc)]
    down = df[(df["FDR"] < fdr) & (df["logFC"] < -logfc)]

    outdir = Path(outdir)

    up.to_csv(outdir / "upregulated.csv", index=False)
    down.to_csv(outdir / "downregulated.csv", index=False)

    summary = outdir / "summary.txt"
    with summary.open("w", encoding="utf-8") as f:
        f.write("=== Differential Expression Summary ===\n\n")
        f.write(f"Total genes: {len(df)}\n")
        f.write(f"FDR cutoff: {fdr}\n")
        f.write(f"logFC cutoff: {logfc}\n")
        f.write(f"Upregulated: {len(up)}\n")
        f.write(f"Downregulated: {len(down)}\n")

    return {
        "results": str(results_file),
        "upregulated": str(outdir / "upregulated.csv"),
        "downregulated": str(outdir / "downregulated.csv"),
        "summary": str(summary),
    }


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def run_differential_expression(config=None, **kwargs):

    if config is None:
        config = DifferentialExpressionConfig(**kwargs)
    elif kwargs:
        raise ValueError("Use config OR kwargs, not both")

    if shutil.which("Rscript") is None:
        raise RuntimeError("Rscript not found")

    outdir = Path(config.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    results_file = outdir / "DE_results.csv"
    norm_file = outdir / "normalized_cpm.csv"

    if results_file.exists() and not config.overwrite:
        print("✔ DEG already exists, skipping")
        return _write_deg_outputs(results_file, outdir, config.fdr, config.logfc)

    # -----------------------------
    # LOAD DATA (kept as-is)
    # -----------------------------
    counts = pd.read_csv(config.counts, index_col=0)
    metadata = pd.read_csv(config.metadata)

    # -----------------------------
    # TEMP R SCRIPT
    # -----------------------------
    def _edgeR_script():
        return r'''
args <- commandArgs(trailingOnly=TRUE)

counts_file <- args[[1]]
metadata_file <- args[[2]]
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
metadata <- read.csv(metadata_file)

metadata[[sample_col]] <- as.character(metadata[[sample_col]])
metadata[[condition_col]] <- as.character(metadata[[condition_col]])

metadata <- metadata[metadata[[condition_col]] %in% c(control, treatment), ]
counts <- counts[, metadata[[sample_col]], drop=FALSE]

group <- factor(metadata[[condition_col]], levels=c(control, treatment))
y <- DGEList(counts, group=group)

keep <- rowSums(cpm(y) > min_count) >= min_samples
y <- y[keep, , keep.lib.sizes=FALSE]

y <- calcNormFactors(y)
design <- model.matrix(~ group)

y <- estimateDisp(y, design)
fit <- glmQLFit(y, design)
qlf <- glmQLFTest(fit, coef=2)

res <- topTags(qlf, n=Inf)$table
res$gene_id <- rownames(res)

write.csv(res, out_results, row.names=FALSE)

norm <- cpm(y, normalized.lib.sizes=TRUE)
write.csv(data.frame(gene_id=rownames(norm), norm), out_norm, row.names=FALSE)
'''

    # write R script
    with tempfile.NamedTemporaryFile("w", suffix=".R", delete=False) as f:
        f.write(_edgeR_script())
        script_path = f.name

    cmd = [
        "Rscript",
        "--vanilla",
        script_path,
        config.counts,
        config.metadata,
        config.sample_col,
        config.condition_col,
        config.control or "",
        config.treatment or "",
        str(results_file),
        str(norm_file),
        str(config.min_count),
        str(config.min_samples),
    ]

    print(f"Running DEG: {config.treatment} vs {config.control}")

    try:
        subprocess.run(cmd, check=True)
    finally:
        try:
            os.remove(script_path)
        except:
            pass

    outputs = _write_deg_outputs(results_file, outdir, config.fdr, config.logfc)
    outputs["normalized_cpm"] = str(norm_file)

    print("✔ DEG complete")
    return outputs


def run_edger():
    return run_differential_expression()
    