import shutil
import subprocess
from pathlib import Path

from pranomics.modules.fastq import find_fastq_pair
from pranomics.utils.auto_installer import install_tool


def run_trimming(sample, samples_dir="data", threads=4):

    Path("trimmed").mkdir(exist_ok=True)

    r1, r2 = find_fastq_pair(sample, samples_dir)

    p1 = Path("trimmed") / f"{sample}_1P.fastq"
    u1 = Path("trimmed") / f"{sample}_1U.fastq"
    p2 = Path("trimmed") / f"{sample}_2P.fastq"
    u2 = Path("trimmed") / f"{sample}_2U.fastq"

    if p1.exists() and p2.exists():
        print(f"Trimming already complete for {sample}")
        return p1, p2

    trimmomatic = shutil.which("trimmomatic")

    # -----------------------------
    # AUTO FIX SECTION
    # -----------------------------
    if not trimmomatic:
        print("⚠ Trimmomatic missing → installing automatically...")

        success = install_tool("trimmomatic")

        trimmomatic = shutil.which("trimmomatic")

        if not trimmomatic:
            raise RuntimeError(
                "Trimmomatic installation failed. Manual setup required."
            )

    cmd = [
        trimmomatic,
        "PE",
        "-threads",
        str(threads),
        str(r1),
        str(r2),
        str(p1),
        str(u1),
        str(p2),
        str(u2),
        "SLIDINGWINDOW:4:15",
        "LEADING:3",
        "TRAILING:3",
        "MINLEN:36",
    ]

    print(f"🧬 Trimming sample {sample}")
    subprocess.run(cmd, check=True)

    return p1, p2

