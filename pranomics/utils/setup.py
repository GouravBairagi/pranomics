import os

def setup_environment():
    os.makedirs("data", exist_ok=True)
    os.makedirs("fastq", exist_ok=True)
    os.makedirs("counts", exist_ok=True)
    os.makedirs("DEG", exist_ok=True)
    os.makedirs("report", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
