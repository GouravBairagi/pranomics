import os
import shutil
import subprocess
import sys


# -----------------------------
# FIND CONDA
# -----------------------------
def _find_conda():
    conda = shutil.which("conda")
    if conda:
        return conda

    possible_paths = [
        os.path.expanduser("~/miniconda3/bin/conda"),
        os.path.expanduser("~/anaconda3/bin/conda"),
        "/opt/miniconda3/bin/conda",
        "/opt/anaconda3/bin/conda",
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    return None


# -----------------------------
# FIX CONDA (TOS + CHANNELS)
# -----------------------------
def _configure_conda(conda_path):
    """
    Auto-fix conda so it works on ANY fresh system:
    - accept TOS
    - set channels
    - enable strict priority
    """

    print("\n🔧 Configuring conda for first-time use...")

    cmds = [
        # accept TOS (safe to re-run)
        [conda_path, "tos", "accept", "--override-channels", "--channel", "https://repo.anaconda.com/pkgs/main"],
        [conda_path, "tos", "accept", "--override-channels", "--channel", "https://repo.anaconda.com/pkgs/r"],

        # required bioinformatics channels
        [conda_path, "config", "--add", "channels", "conda-forge"],
        [conda_path, "config", "--add", "channels", "bioconda"],
        [conda_path, "config", "--set", "channel_priority", "strict"],
    ]

    for cmd in cmds:
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            # ignore failures (already configured systems)
            pass

    print("✔ Conda configured successfully")


# -----------------------------
# MAIN BOOTSTRAP
# -----------------------------
def ensure_conda(skip_install=False):
    conda_path = _find_conda()

    if not conda_path:
        print("\n❌ Conda not found")
        print("👉 Install Miniconda: https://docs.conda.io/en/latest/miniconda.html")

        if skip_install:
            raise RuntimeError("Conda missing and skip_install=True")

        raise RuntimeError("Conda is required")

    # fix PATH
    conda_dir = os.path.dirname(conda_path)
    os.environ["PATH"] = conda_dir + ":" + os.environ["PATH"]

    print(f"\n✔ Conda detected at: {conda_path}")

    # IMPORTANT: auto-fix conda for any system
    _configure_conda(conda_path)

    print("✔ Conda environment ready")

    return conda_path
