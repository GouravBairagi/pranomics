import os
import shutil
import subprocess
import sys
from pathlib import Path


def create_sample_list(samples, path="sample_list.txt"):
    with open(path, "w", encoding="utf-8") as handle:
        for sample in samples:
            gtf = Path("stringtie") / f"{sample}.gtf"
            if not gtf.exists():
                raise FileNotFoundError(f"StringTie GTF missing for {sample}: {gtf}")
            handle.write(f"{sample}\t{gtf}\n")
    print(f"Sample list written: {path}")
    return path


def _find_prepde():
    executable = shutil.which("prepDE.py3") or shutil.which("prepDE.py")
    if executable:
        return executable

    conda_prefix = os.environ.get("CONDA_PREFIX")
    if conda_prefix:
        matches = list(Path(conda_prefix).rglob("prepDE.py3")) + list(
            Path(conda_prefix).rglob("prepDE.py")
        )
        if matches:
            return str(matches[0])

    raise FileNotFoundError(
        "prepDE.py3 was not found. Install stringtie from bioconda or provide it on PATH."
    )


def run_prepde(sample_list="sample_list.txt"):
    Path("counts").mkdir(exist_ok=True)
    gene_matrix = Path("counts") / "gene_count_matrix.csv"
    transcript_matrix = Path("counts") / "transcript_count_matrix.csv"

    if gene_matrix.exists() and transcript_matrix.exists():
        print("Count matrices already exist")
        return gene_matrix, transcript_matrix

    prepde = _find_prepde()
    print("Generating count matrices with prepDE")
    subprocess.run(
        [
            sys.executable,
            prepde,
            "-i",
            sample_list,
            "-g",
            str(gene_matrix),
            "-t",
            str(transcript_matrix),
        ],
        check=True,
    )
    return gene_matrix, transcript_matrix
