PIPELINE_STEPS = [
    "SRA -> FASTQ",
    "FASTQC",
    "TRIMMING",
    "BOWTIE2 INDEX",
    "ALIGNMENT",
    "BAM PROCESSING",
    "SORTING",
    "STRINGTIE",
    "COUNT MATRIX",
    "DEG ANALYSIS",
    "VISUALIZATION",
    "REPORT",
]


def show_pipeline_flow():
    print("\nPIPELINE FLOW\n")

    for step in PIPELINE_STEPS:
        print(f"   - {step}")

    print()
