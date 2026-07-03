import os
from rich.progress import track

from pranomics.modules.alignment import align_sample, build_index
from pranomics.modules.bam_processing import sam_to_bam
from pranomics.modules.count_matrix import create_sample_list, run_prepde
from pranomics.modules.differential_expression import (
    DifferentialExpressionConfig,
    run_differential_expression,
)
from pranomics.modules.fastq import convert_sra_to_fastq
from pranomics.modules.fastqc import run_fastqc
from pranomics.modules.final_report import generate_final_report
from pranomics.modules.heatmap import run_heatmap
from pranomics.modules.html_report import generate_html_report
from pranomics.modules.interactive_plotly import create_interactive_volcano
from pranomics.modules.pca import run_pca
from pranomics.modules.sorting import sort_bam
from pranomics.modules.stringtie_module import run_stringtie
from pranomics.modules.trimming import run_trimming

from pranomics.utils.UI import banner, info, section, success, warning
from pranomics.utils.tool_manager import install_missing
from pranomics.utils.conda_bootstrap import ensure_conda
from pranomics.utils.flow import show_pipeline_flow
from pranomics.utils.reference_manager import validate_reference
from pranomics.utils.sample_discovery import discover_samples
from pranomics.environment import setup_environment
from pranomics.utils.validators import validate_environment, validate_metadata
from pranomics.utils.checkpoint import is_done, mark_done
from pranomics.utils.paths import Paths


# =========================================================
# ENV VALIDATION + INSTALL
# =========================================================
def _validate_or_install(skip_install=False):

    section("ENVIRONMENT VALIDATION")

    report = validate_environment()

    missing = (
        report["missing_tools"]
        or report["missing_r_packages"]
        or report["missing_python_packages"]
    )

    if not missing:
        success("Environment ready")
        return

    if skip_install:
        raise RuntimeError("Missing dependencies + skip_install=True")

    warning("Missing dependencies detected")

    choice = input("Install missing dependencies? (y/n): ").strip().lower()

    if choice != "y":
        raise RuntimeError("User aborted installation")

    install_missing(report)

    report = validate_environment()

    still_missing = (
        report["missing_tools"]
        or report["missing_r_packages"]
        or report["missing_python_packages"]
    )

    if still_missing:
        print("\n⚠ WARNING: Some dependencies still missing after install attempt:")
        print("Tools:", report["missing_tools"])
        print("R packages:", report["missing_r_packages"])
        print("Python packages:", report["missing_python_packages"])
        print("\n👉 Continuing pipeline in degraded mode (some steps may fail)\n")

    return


# =========================================================
# SAFE STEP WITH RESUME
# =========================================================
def run_step_with_resume(step, sample, func, *args, **kwargs):

    if is_done(sample, step):
        print(f"✓ SKIP {step} ({sample})")
        return None

    result = func(*args, **kwargs)

    mark_done(sample, step)

    return result


# =========================================================
# PIPELINE
# =========================================================
def run_pipeline(
    samples_dir=None,
    reference_dir=None,
    reference=None,
    gff_file=None,
    threads=4,
    metadata=None,
    sample_col="sample",
    condition_col="condition",
    control=None,
    treatment=None,
    skip_install=False,
    overwrite_deg=False,
    base_dir=None,
):

    banner()

    # ---------------- PATH SYSTEM ----------------
    paths = Paths(base_dir).create_all()

    section("PIPELINE INITIALIZATION")

    setup_environment()

    section("BOOTSTRAP ENVIRONMENT")

    ensure_conda(skip_install=skip_install)

    _validate_or_install(skip_install=skip_install)

    show_pipeline_flow()

    # ---------------- SAMPLE DISCOVERY ----------------
    section("SAMPLE DISCOVERY")

    samples, sample_type = discover_samples(
        samples_dir or str(paths.data)
    )

    info(f"{len(samples)} samples detected ({sample_type})")

    # ---------------- METADATA ----------------
    section("METADATA VALIDATION")

    validate_metadata(
        metadata,
        samples,
        sample_col,
        condition_col
    )

    # ---------------- REFERENCE ----------------
    section("REFERENCE VALIDATION")

    if reference and gff_file:
        fasta, gff = reference, gff_file
    else:
        fasta, gff = validate_reference(
            reference_dir or str(paths.reference)
        )

    success(f"FASTA: {fasta}")
    success(f"GFF: {gff}")

    # ---------------- FASTQ ----------------
    section("READ PROCESSING")

    for s in track(samples, description="FASTQ"):
        run_step_with_resume("FASTQ", s, convert_sra_to_fastq, s, str(paths.data))

    for s in track(samples, description="FASTQC"):
        run_step_with_resume("FASTQC", s, run_fastqc, s, str(paths.data))

    for s in track(samples, description="TRIMMING"):
        run_step_with_resume("TRIMMING", s, run_trimming, s, str(paths.data), threads)

    # ---------------- ALIGNMENT ----------------
    section("ALIGNMENT")

    index = build_index(fasta)

    for s in track(samples, description="ALIGNMENT"):
        run_step_with_resume("ALIGNMENT", s, align_sample, s, index, threads)

    # ---------------- BAM ----------------
    section("BAM PROCESSING")

    for s in track(samples, description="SAM→BAM"):
        run_step_with_resume("BAM", s, sam_to_bam, s)

    for s in track(samples, description="SORTING"):
        run_step_with_resume("SORT", s, sort_bam, s, threads)

    # ---------------- COUNTING ----------------
    section("GENE COUNTING")

    for s in track(samples, description="STRINGTIE"):
        run_step_with_resume("STRINGTIE", s, run_stringtie, s, gff, threads)

    sample_list = create_sample_list(samples)
    run_prepde(sample_list)

    # ---------------- DEG ----------------
    section("DIFFERENTIAL EXPRESSION")

    config = DifferentialExpressionConfig(
        counts=str(paths.counts / "gene_count_matrix.csv"),
        metadata=metadata,
        outdir=str(paths.deg),
        sample_col=sample_col,
        condition_col=condition_col,
        control=control,
        treatment=treatment,
        overwrite=overwrite_deg,
    )

    run_differential_expression(config)

    # ---------------- VISUALIZATION ----------------
    section("VISUALIZATION")

    if not is_done("GLOBAL", "PCA"):
        run_pca(metadata=metadata)
        mark_done("GLOBAL", "PCA")

    if not is_done("GLOBAL", "HEATMAP"):
        run_heatmap(metadata=metadata)
        mark_done("GLOBAL", "HEATMAP")

    if not is_done("GLOBAL", "VOLCANO"):
        create_interactive_volcano()
        mark_done("GLOBAL", "VOLCANO")

    # ---------------- REPORT ----------------
    section("REPORT")

    required_files = [
        str(paths.deg / "pca.png"),
        str(paths.deg / "heatmap.png"),
        str(paths.report / "interactive" / "volcano.html"),
        str(paths.counts / "gene_count_matrix.csv"),
    ]

    missing_files = [f for f in required_files if not os.path.exists(f)]

    if missing_files:
        warning(f"Report skipped: missing files {missing_files}")
        return

    if not is_done("GLOBAL", "REPORT"):
        try:
            generate_final_report()
            generate_html_report("RNA-seq pipeline completed")
            mark_done("GLOBAL", "REPORT")
            success("REPORT GENERATED")

        except Exception as e:
            warning(f"REPORT FAILED: {e}")
            raise RuntimeError("Pipeline failed at report stage")

    success("PIPELINE COMPLETED SUCCESSFULLY")
    