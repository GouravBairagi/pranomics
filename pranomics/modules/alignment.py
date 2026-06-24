import subprocess
from pathlib import Path


def build_index(reference, index_dir="reference/index"):
    index_path = Path(index_dir)
    index_path.mkdir(parents=True, exist_ok=True)
    index_prefix = index_path / "genome"

    if (index_path / "genome.1.bt2").exists() or (index_path / "genome.1.bt2l").exists():
        print("Bowtie2 index already exists")
        return str(index_prefix)

    print(f"Building Bowtie2 index from {reference}")
    subprocess.run(["bowtie2-build", str(reference), str(index_prefix)], check=True)
    return str(index_prefix)


def align_sample(sample, index_prefix="reference/index/genome", threads=4):
    Path("alignments").mkdir(exist_ok=True)
    r1 = Path("trimmed") / f"{sample}_1P.fastq"
    r2 = Path("trimmed") / f"{sample}_2P.fastq"
    out = Path("alignments") / f"{sample}.sam"

    if out.exists():
        print(f"Alignment already complete for {sample}")
        return out

    if not r1.exists() or not r2.exists():
        raise FileNotFoundError(f"Trimmed FASTQ pair missing for {sample}")

    print(f"Aligning sample {sample}")
    subprocess.run(
        [
            "bowtie2",
            "-x",
            str(index_prefix),
            "-1",
            str(r1),
            "-2",
            str(r2),
            "-S",
            str(out),
            "-p",
            str(threads),
        ],
        check=True,
    )
    return out
