import subprocess
from pathlib import Path


def run_stringtie(sample, gff_file, threads=4):
    Path("stringtie").mkdir(exist_ok=True)
    bam = Path("sorted_bam") / f"{sample}.sorted.bam"
    out = Path("stringtie") / f"{sample}.gtf"

    if out.exists():
        print(f"StringTie already complete for {sample}")
        return out

    if not bam.exists():
        raise FileNotFoundError(f"Sorted BAM missing for {sample}")

    print(f"Running StringTie for {sample}")
    subprocess.run(
        [
            "stringtie",
            str(bam),
            "-G",
            str(gff_file),
            "-o",
            str(out),
            "-p",
            str(threads),
            "-e",
            "-B",
        ],
        check=True,
    )
    return out
