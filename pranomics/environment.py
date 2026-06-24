import shutil


def setup_environment():

    print("\n🧪 Checking environment...\n")

    tools = [
        "fastqc",
        "bowtie2",
        "samtools",
        "stringtie"
    ]

    for tool in tools:
        if shutil.which(tool):
            print(f"✔ {tool}")
        else:
            print(f"⚠ {tool} not found")

    print("\n✅ Environment check finished")
    