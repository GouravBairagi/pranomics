import subprocess
from pathlib import Path

from pranomics.modules.fastq import find_fastq_pair


def run_fastqc(sample, samples_dir="data"):
    Path("fastqc").mkdir(exist_ok=True)
    r1, r2 = find_fastq_pair(sample, samples_dir)

    html = Path("fastqc") / f"{Path(r1).name.removesuffix('.gz').replace('.fastq', '')}_fastqc.html"
    if html.exists():
        print(f"FASTQC already complete for {sample}")
        return

    print(f"Running FASTQC for {sample}")
    subprocess.run(["fastqc", str(r1), str(r2), "-o", "fastqc"], check=True)
