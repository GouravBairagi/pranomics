import subprocess
from pathlib import Path

from pranomics.utils.paths import Paths


def run_heatmap(
    counts="counts/gene_count_matrix.csv",
    metadata="metadata/metadata.csv",
    base_dir=None
):

    paths = Paths(base_dir)

    out = paths.deg / "heatmap.png"

    if out.exists():
        print("✓ Heatmap already exists")
        return str(out)

    script = paths.base / "scripts" / "heatmap.R"

    # ensure output directory exists
    paths.deg.mkdir(parents=True, exist_ok=True)

    cmd = [
        "Rscript",
        str(script),
        str(paths.base / counts),
        str(paths.base / metadata),
        str(out),
    ]

    print("🧊 Running Heatmap...")

    subprocess.run(cmd, check=True)

    return str(out)