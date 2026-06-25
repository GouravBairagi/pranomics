import argparse
from pathlib import Path

from pranomics.modules.differential_expression import (
    DifferentialExpressionConfig,
    run_differential_expression,
)

from pranomics.utils.metadata_discovery import discover_metadata
from pranomics.pipeline import run_pipeline


# =====================================================
# PIPELINE ARGUMENTS
# =====================================================

def add_pipeline_args(parser):

    parser.add_argument(
        "--samples",
        default="data",
        help="FASTQ/SRA input directory"
    )

    parser.add_argument(
        "--metadata",
        default=None,
        help="Metadata CSV file"
    )

    parser.add_argument(
        "--reference-dir",
        default="reference"
    )

    parser.add_argument(
        "--reference",
        default=None
    )

    parser.add_argument(
        "--gff",
        default=None
    )

    parser.add_argument(
        "--threads",
        type=int,
        default=4
    )

    parser.add_argument(
        "--sample-col",
        default="sample"
    )

    parser.add_argument(
        "--condition-col",
        default="condition"
    )

    parser.add_argument(
        "--control"
    )

    parser.add_argument(
        "--treatment"
    )

    parser.add_argument(
        "--skip-install",
        action="store_true"
    )

    parser.add_argument(
        "--overwrite-deg",
        action="store_true"
    )


# =====================================================
# DEG ARGUMENTS
# =====================================================

def add_deg_args(parser):

    parser.add_argument(
        "--counts",
        default="counts/gene_count_matrix.csv"
    )

    parser.add_argument(
        "--metadata",
        default="metadata/metadata.csv"
    )

    parser.add_argument(
        "--outdir",
        default="DEG"
    )

    parser.add_argument(
        "--sample-col",
        default="sample"
    )

    parser.add_argument(
        "--condition-col",
        default="condition"
    )

    parser.add_argument(
        "--control"
    )

    parser.add_argument(
        "--treatment"
    )

    parser.add_argument(
        "--fdr",
        type=float,
        default=0.05
    )

    parser.add_argument(
        "--logfc",
        type=float,
        default=1.0
    )

    parser.add_argument(
        "--min-count",
        type=int,
        default=10
    )

    parser.add_argument(
        "--min-samples",
        type=int,
        default=2
    )

    parser.add_argument(
        "--overwrite",
        action="store_true"
    )


# =====================================================
# INIT PROJECT
# =====================================================

def run_init():

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

        Path(folder).mkdir(
            parents=True,
            exist_ok=True
        )

        print(f"✔ Created {folder}/")


    metadata = Path(
        "metadata/metadata.csv"
    )


    if not metadata.exists():

        metadata.write_text(
            "sample,condition\n"
            "sample1,control\n"
            "sample2,control\n"
            "sample3,treatment\n"
            "sample4,treatment\n"
        )

        print(
            "✔ Created metadata/metadata.csv"
        )


    print(
        "\n✅ Pranomics project initialized\n"
    )



# =====================================================
# AUTO PIPELINE
# =====================================================

def run_auto_pipeline():

    print(
        "\n🚀 Running automatic Pranomics pipeline\n"
    )


    metadata = discover_metadata()


    run_pipeline(

        samples_dir="data",

        metadata=metadata,

        reference_dir="reference"

    )



# =====================================================
# MANUAL PIPELINE
# =====================================================

def run_pipeline_from_args(args):

    metadata = (
        args.metadata
        if args.metadata
        else discover_metadata()
    )


    run_pipeline(

        samples_dir=args.samples,

        reference_dir=args.reference_dir,

        reference=args.reference,

        gff_file=args.gff,

        threads=args.threads,

        metadata=metadata,

        sample_col=args.sample_col,

        condition_col=args.condition_col,

        control=args.control,

        treatment=args.treatment,

        skip_install=args.skip_install,

        overwrite_deg=args.overwrite_deg

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
# MAIN CLI
# =====================================================

def main():


    parser = argparse.ArgumentParser(

        prog="pranomics",

        description=
        "Pranomics RNA-seq Pipeline (FASTQ → DEG → Report)"

    )


    subparsers = parser.add_subparsers(
        dest="command"
    )


    pipeline_parser = subparsers.add_parser(
        "pipeline",
        help="Run complete RNA-seq pipeline"
    )

    add_pipeline_args(
        pipeline_parser
    )



    deg_parser = subparsers.add_parser(
        "deg",
        help="Run only differential expression"
    )

    add_deg_args(
        deg_parser
    )



    subparsers.add_parser(
        "run",
        help="Automatically detect inputs and run pipeline"
    )


    subparsers.add_parser(
        "init",
        help="Create Pranomics project structure"
    )



    args = parser.parse_args()



    if args.command == "pipeline":

        run_pipeline_from_args(args)



    elif args.command == "deg":

        run_deg_from_args(args)



    elif args.command == "init":

        run_init()



    elif args.command == "run":

        run_auto_pipeline()



    else:

        parser.print_help()



if __name__ == "__main__":

    main()
    