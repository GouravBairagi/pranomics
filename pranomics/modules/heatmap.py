import subprocess
from pathlib import Path
from pranomics.utils.paths import PROJECT_ROOT, SCRIPTS_DIR, DEG_DIR


def run_heatmap(counts="counts/gene_count_matrix.csv", metadata="metadata.csv"):

    DEG_DIR.mkdir(exist_ok=True)

    out = DEG_DIR / "heatmap.png"

    if out.exists():
        print("✓ Heatmap already exists")
        return str(out)

    script = SCRIPTS_DIR / "heatmap.R"

    cmd = [
        "Rscript",
        str(script),
        str(PROJECT_ROOT / counts),
        str(PROJECT_ROOT / metadata),
        str(out),
    ]

    print("🧊 Running Heatmap...")
    subprocess.run(cmd, check=True)

    return str(out)
