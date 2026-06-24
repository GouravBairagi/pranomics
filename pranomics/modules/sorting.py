import subprocess
from pathlib import Path


def sort_bam(sample, threads=4):
    Path("sorted_bam").mkdir(exist_ok=True)
    bam_in = Path("bam") / f"{sample}.bam"
    bam_out = Path("sorted_bam") / f"{sample}.sorted.bam"

    if bam_out.exists():
        print(f"Sorted BAM already exists for {sample}")
        return bam_out

    if not bam_in.exists():
        raise FileNotFoundError(f"BAM file missing for {sample}")

    print(f"Sorting BAM for {sample}")
    subprocess.run(
        ["samtools", "sort", "-@", str(threads), str(bam_in), "-o", str(bam_out)],
        check=True,
    )
    subprocess.run(["samtools", "index", str(bam_out)], check=True)
    return bam_out
