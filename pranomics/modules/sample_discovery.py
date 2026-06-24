from glob import glob
import os


def discover_samples(data_dir):

    sra_files = glob(f"{data_dir}/*.sra")

    samples = []

    for file in sra_files:

        sample_name = os.path.basename(file)

        sample_name = os.path.splitext(sample_name)[0]

        samples.append(sample_name)

    return sorted(samples)