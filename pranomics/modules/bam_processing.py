import subprocess
from pathlib import Path


def sam_to_bam(sample):
    Path("bam").mkdir(exist_ok=True)
    sam_file = Path("alignments") / f"{sample}.sam"
    bam_file = Path("bam") / f"{sample}.bam"

    if bam_file.exists():
        print(f"BAM already exists for {sample}")
        return bam_file

    if not sam_file.exists():
        raise FileNotFoundError(f"SAM file missing for {sample}")

    print(f"Converting SAM to BAM for {sample}")
    subprocess.run(["samtools", "view", "-Sb", str(sam_file), "-o", str(bam_file)], check=True)
    return bam_file
