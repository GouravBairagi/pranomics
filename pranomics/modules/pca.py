import subprocess
from pathlib import Path


def run_pca(
    counts="counts/gene_count_matrix.csv",
    metadata="metadata/metadata.csv",
):

    deg_dir = Path("DEG")
    deg_dir.mkdir(parents=True, exist_ok=True)

    out = deg_dir / "pca.png"

    if out.exists():
        print("✓ PCA already exists (skipping)")
        return str(out)

    script = Path(__file__).resolve().parents[2] / "scripts" / "pca.R"

    cmd = [
        "Rscript",
        str(script),
        str(Path(counts).resolve()),
        str(Path(metadata).resolve()),
        str(out.resolve()),
    ]

    print("📈 Running PCA...")
    subprocess.run(cmd, check=True)

    return str(out)
    