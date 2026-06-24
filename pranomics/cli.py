import argparse
import os
from pathlib import Path

from pranomics.modules.differential_expression import (
DifferentialExpressionConfig,
run_differential_expression,
)

from pranomics.utils.metadata_discovery import discover_metadata
from pranomics.pipeline import run_pipeline

# -----------------------------

# PIPELINE ARGS

# -----------------------------

def add_pipeline_args(parser):
parser.add_argument("--samples", default="data")
parser.add_argument("--metadata", default=None)

```
parser.add_argument("--reference-dir", default="reference")
parser.add_argument("--reference", default=None)
parser.add_argument("--gff", default=None)

parser.add_argument("--threads", type=int, default=4)

parser.add_argument("--sample-col", default="sample")
parser.add_argument("--condition-col", default="condition")

parser.add_argument("--control")
parser.add_argument("--treatment")

parser.add_argument("--skip-install", action="store_true")
parser.add_argument("--overwrite-deg", action="store_true")
```

# -----------------------------

# DEG ARGS

# -----------------------------

def add_deg_args(parser):
parser.add_argument("--counts", default="counts/gene_count_matrix.csv")
parser.add_argument("--metadata", default="metadata/metadata.csv")
parser.add_argument("--outdir", default="DEG")

```
parser.add_argument("--sample-col", default="sample")
parser.add_argument("--condition-col", default="condition")

parser.add_argument("--control")
parser.add_argument("--treatment")

parser.add_argument("--fdr", type=float, default=0.05)
parser.add_argument("--logfc", type=float, default=1.0)

parser.add_argument("--min-count", type=int, default=10)
parser.add_argument("--min-samples", type=int, default=2)

parser.add_argument("--overwrite", action="store_true")
```

# -----------------------------

# INIT PROJECT (NEW)

# -----------------------------

def run_init():
print("\n🧬 Initializing Pranomics project...\n")

```
folders = [
    "data",
    "metadata",
    "reference",
    "counts",
    "DEG",
    "report",
    "logs"
]

for f in folders:
    Path(f).mkdir(parents=True, exist_ok=True)
    print(f"✔ Created: {f}/")

metadata = Path("metadata/metadata.csv")

if not metadata.exists():
    metadata.write_text(
        "sample,condition\n"
        "sample1,control\n"
        "sample2,control\n"
        "sample3,treated\n"
        "sample4,treated\n"
    )
    print("✔ Created: metadata/metadata.csv")

print("\n✅ Pranomics project initialized successfully!\n")
```

# -----------------------------

# AUTO PIPELINE

# -----------------------------

def run_auto_pipeline():
metadata = discover_metadata()

```
run_pipeline(
    samples_dir="data",
    metadata=metadata,
    reference_dir="reference",
)
```

# -----------------------------

# PIPELINE RUNNER (MANUAL)

# -----------------------------

def run_pipeline_from_args(args):
metadata = args.metadata or discover_metadata()

```
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
    overwrite_deg=args.overwrite_deg,
)
```

# -----------------------------

# DEG RUNNER

# -----------------------------

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

```
run_differential_expression(config)
```

# -----------------------------

# MAIN CLI

# -----------------------------

def main():
parser = argparse.ArgumentParser(
prog="pranomics",
description="Automated RNA-seq Pipeline (FASTQ → DEG → Report)",
)

```
subparsers = parser.add_subparsers(dest="command")

# pipeline
pipeline_parser = subparsers.add_parser("pipeline")
add_pipeline_args(pipeline_parser)

# deg
deg_parser = subparsers.add_parser("deg")
add_deg_args(deg_parser)

# run (AUTO)
subparsers.add_parser("run", help="Auto-detect and run full pipeline")

# init
subparsers.add_parser("init", help="Initialize project structure")

args = parser.parse_args()

# -------------------------
# ROUTER
# -------------------------
if args.command == "deg":
    run_deg_from_args(args)

elif args.command == "run":
    run_auto_pipeline()

elif args.command == "init":
    run_init()

else:
    run_auto_pipeline()
```

if **name** == "**main**":
main()
