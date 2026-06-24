from pathlib import Path


def discover_samples(data_dir="data"):
    data_path = Path(data_dir)
    if not data_path.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    sra_files = sorted(data_path.glob("*.sra"))
    if sra_files:
        samples = [path.stem for path in sra_files]
        print(f"Found {len(samples)} SRA samples")
        return samples, "sra"

    r1_files = []
    for pattern in ("*_R1*.fastq*", "*_1.fastq*", "*.1.fastq*"):
        r1_files.extend(data_path.glob(pattern))

    if r1_files:
        samples = []
        for path in r1_files:
            name = path.name
            if "_R1" in name:
                sample = name.split("_R1")[0]
            elif "_1" in name:
                sample = name.split("_1")[0]
            else:
                sample = name.split(".1")[0]
            samples.append(sample)

        samples = sorted(set(samples))
        print(f"Found {len(samples)} FASTQ samples")
        return samples, "fastq"

    raise FileNotFoundError(f"No SRA or paired FASTQ files found in {data_dir}")
