import shutil
import subprocess
from pathlib import Path


def find_fastq_pair(sample, samples_dir="data"):
    data_path = Path(samples_dir)
    patterns = [
        (f"{sample}_R1*.fastq*", f"{sample}_R2*.fastq*"),
        (f"{sample}_1.fastq*", f"{sample}_2.fastq*"),
        (f"{sample}.1.fastq*", f"{sample}.2.fastq*"),
    ]

    for r1_pattern, r2_pattern in patterns:
        r1 = sorted(data_path.glob(r1_pattern))
        r2 = sorted(data_path.glob(r2_pattern))
        if r1 and r2:
            return r1[0], r2[0]

    fastq_path = Path("fastq")
    r1 = fastq_path / f"{sample}_1.fastq"
    r2 = fastq_path / f"{sample}_2.fastq"
    if r1.exists() and r2.exists():
        return r1, r2

    raise FileNotFoundError(f"FASTQ pair not found for sample {sample}")


def convert_sra_to_fastq(sample, samples_dir="data"):
    Path("fastq").mkdir(exist_ok=True)

    sra_file = Path(samples_dir) / f"{sample}.sra"
    if not sra_file.exists():
        return find_fastq_pair(sample, samples_dir)

    r1 = Path("fastq") / f"{sample}_1.fastq"
    r2 = Path("fastq") / f"{sample}_2.fastq"
    if r1.exists() and r2.exists():
        print(f"{sample} already converted to FASTQ")
        return r1, r2

    fasterq_dump = shutil.which("fasterq-dump")
    if fasterq_dump:
        command = [fasterq_dump, str(sra_file), "--split-files", "--outdir", "fastq"]
    else:
        command = ["fastq-dump", str(sra_file), "--split-files", "--outdir", "fastq"]

    print(f"Converting {sample} to FASTQ")
    subprocess.run(command, check=True)

    if not (r1.exists() and r2.exists()):
        raise RuntimeError(f"FASTQ files were not generated for {sample}")

    return r1, r2
