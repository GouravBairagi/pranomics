import subprocess
from pathlib import Path
from pranomics.utils.paths import PROJECT_ROOT, DEG_DIR, SCRIPTS_DIR


def run_pca(counts="counts/gene_count_matrix.csv", metadata="metadata.csv"):

    out = DEG_DIR / "pca.png"
    DEG_DIR.mkdir(exist_ok=True)

    if out.exists():
        print("✓ PCA already exists (skipping)")
        return str(out)

    script = SCRIPTS_DIR / "pca.R"

    cmd = [
        "Rscript",
        str(script),
        str(PROJECT_ROOT / counts),
        str(PROJECT_ROOT / metadata),
        str(out),
    ]

    print("📈 Running PCA...")
    subprocess.run(cmd, check=True)

    return str(out)
