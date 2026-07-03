import argparse
import sys

from pranomics.pipeline import run_pipeline
from pranomics.modules.differential_expression import (
    DifferentialExpressionConfig,
    run_differential_expression,
)

from pranomics.utils.metadata_discovery import discover_metadata

# ==============================
# BOOTSTRAP IMPORTS (NEW LAYER)
# ==============================
from pranomics.bootstrap.verify import system_health_check
from pranomics.bootstrap.verify import assert_ready
from pranomics.bootstrap.conda import bootstrap_conda


# =====================================================
# INIT PROJECT
# =====================================================
def run_init():
    """
    Create project structure for RNA-seq workflow
    """

    from pathlib import Path

    print("\n🧬 Initializing Pranomics project...\n")

    folders = [
        "data",
        "metadata",
        "reference",
        "counts",
        "DEG",
        "report",
        "logs"
    ]

    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"✔ Created {folder}/")

    meta_file = Path("metadata/metadata.csv")

    if not meta_file.exists():
        meta_file.write_text(
            "sample,condition\n"
            "sample1,control\n"
            "sample2,control\n"
            "sample3,treatment\n"
            "sample4,treatment\n"
        )
        print("✔ Created metadata/metadata.csv")

    print("\n✅ Project initialized successfully\n")


# =====================================================
# PIPELINE RUNNER
# =====================================================
def run_pipeline_from_args(args):

    metadata = args.metadata or discover_metadata()

    run_pipeline(
        samples_dir=args.samples,
        metadata=metadata,
        reference_dir=args.reference_dir,
        reference=args.reference,
        gff_file=args.gff,
        threads=args.threads,
        sample_col=args.sample_col,
        condition_col=args.condition_col,
        control=args.control,
        treatment=args.treatment,
        skip_install=args.skip_install,
        overwrite_deg=args.overwrite_deg,
    )


# =====================================================
# DEG RUNNER
# =====================================================
def run_deg_from_args(args):

    config = DifferentialExpressionConfig(
        counts=args.counts,
        metadata=args.metadata,
        outdir=args.outdir,
        sample_col=args.sample_col,
        condition_col=args.condition_col,
        control=args.control,
        treatment=args.treatment,
        fdr=args.fdr,
        logfc=args.logfc,
        min_count=args.min_count,
        min_samples=args.min_samples,
        overwrite=args.overwrite,
    )

    run_differential_expression(config)


# =====================================================
# AUTO PIPELINE (SMART MODE)
# =====================================================
def run_auto_pipeline():

    print("\n🚀 Auto-detecting inputs and running pipeline...\n")

    metadata = discover_metadata()

    run_pipeline(
        samples_dir="data",
        metadata=metadata,
        reference_dir="reference",
    )


# =====================================================
# CLI BUILDER
# =====================================================
def main():

    parser = argparse.ArgumentParser(
        prog="pranomics",
        description="Pranomics RNA-seq Pipeline (FASTQ → DEG → Report)"
    )

    sub = parser.add_subparsers(dest="command")

    # -----------------------------
    # PIPELINE COMMAND
    # -----------------------------
    p_pipeline = sub.add_parser("pipeline")
    p_pipeline.add_argument("--samples", default="data")
    p_pipeline.add_argument("--metadata", default=None)
    p_pipeline.add_argument("--reference-dir", default="reference")
    p_pipeline.add_argument("--reference", default=None)
    p_pipeline.add_argument("--gff", default=None)
    p_pipeline.add_argument("--threads", type=int, default=4)
    p_pipeline.add_argument("--sample-col", default="sample")
    p_pipeline.add_argument("--condition-col", default="condition")
    p_pipeline.add_argument("--control")
    p_pipeline.add_argument("--treatment")
    p_pipeline.add_argument("--skip-install", action="store_true")
    p_pipeline.add_argument("--overwrite-deg", action="store_true")

    # -----------------------------
    # DEG COMMAND
    # -----------------------------
    p_deg = sub.add_parser("deg")
    p_deg.add_argument("--counts", default="counts/gene_count_matrix.csv")
    p_deg.add_argument("--metadata", default="metadata/metadata.csv")
    p_deg.add_argument("--outdir", default="DEG")
    p_deg.add_argument("--sample-col", default="sample")
    p_deg.add_argument("--condition-col", default="condition")
    p_deg.add_argument("--control")
    p_deg.add_argument("--treatment")
    p_deg.add_argument("--fdr", type=float, default=0.05)
    p_deg.add_argument("--logfc", type=float, default=1.0)
    p_deg.add_argument("--min-count", type=int, default=10)
    p_deg.add_argument("--min-samples", type=int, default=2)
    p_deg.add_argument("--overwrite", action="store_true")

    # -----------------------------
    # SIMPLE COMMANDS
    # -----------------------------
    sub.add_parser("init")
    sub.add_parser("run")
    sub.add_parser("check")
    sub.add_parser("bootstrap")

    args = parser.parse_args()

    # =================================================
    # ROUTER
    # =================================================

    if args.command == "init":
        run_init()

    elif args.command == "pipeline":
        run_pipeline_from_args(args)

    elif args.command == "deg":
        run_deg_from_args(args)

    elif args.command == "run":
        run_auto_pipeline()

    elif args.command == "check":
        system_health_check()

    elif args.command == "bootstrap":
        bootstrap_conda()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
    