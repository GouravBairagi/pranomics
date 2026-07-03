import os
import subprocess
import sys
import platform
from pathlib import Path

from pranomics.bootstrap.downloader import safe_download
from pranomics.bootstrap.internet import wait_for_internet
from pranomics.bootstrap.verify import _check_os


# =====================================================
# MINICONDA CONFIG
# =====================================================
MINICONDA_URLS = {
    "Linux": "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh",
    "Darwin": "https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh",
    "Windows": "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe",
}


ENV_NAME = "pranomics"


# =====================================================
# FIND CONDA
# =====================================================
def find_conda():
    return shutil_which("conda")


def shutil_which(cmd):
    from shutil import which
    return which(cmd)


# =====================================================
# INSTALL MINICONDA
# =====================================================
def install_miniconda():
    """
    Downloads and installs Miniconda silently if missing.
    """

    system = platform.system()

    if system not in MINICONDA_URLS:
        raise RuntimeError(f"Unsupported OS: {system}")

    url = MINICONDA_URLS[system]

    print("\n⬇ Downloading Miniconda...")

    installer_path = safe_download(
        url,
        f"/tmp/miniconda_installer.{system}"
    )

    print("\n⚙ Installing Miniconda...")

    if system == "Linux":
        subprocess.run(
            ["bash", installer_path, "-b", "-p", str(Path.home() / "miniconda3")],
            check=True
        )

    elif system == "Darwin":
        subprocess.run(
            ["bash", installer_path, "-b", "-p", str(Path.home() / "miniconda3")],
            check=True
        )

    elif system == "Windows":
        subprocess.run([installer_path, "/S", "/D=C:\\Miniconda3"], check=True)

    print("✔ Miniconda installed")


# =====================================================
# CONFIGURE CONDA CHANNELS
# =====================================================
def configure_conda(conda_path):
    """
    Sets up bioconda environment properly
    """

    print("\n🔧 Configuring Conda channels...")

    cmds = [
        [conda_path, "config", "--add", "channels", "conda-forge"],
        [conda_path, "config", "--add", "channels", "bioconda"],
        [conda_path, "config", "--set", "channel_priority", "strict"],
    ]

    for cmd in cmds:
        try:
            subprocess.run(cmd, check=True)
        except Exception:
            pass

    print("✔ Conda configured")


# =====================================================
# CREATE ENVIRONMENT
# =====================================================
def create_env(conda_path, env_file=None):
    """
    Creates pranomics conda environment
    """

    print("\n🧬 Creating Pranomics environment...")

    if env_file:
        subprocess.run(
            [conda_path, "env", "create", "-f", env_file],
            check=True
        )
    else:
        subprocess.run(
            [conda_path, "create", "-y", "-n", ENV_NAME, "python=3.10"],
            check=True
        )

    print(f"✔ Environment ready: {ENV_NAME}")


# =====================================================
# ACTIVATE HELP TEXT
# =====================================================
def activation_instructions():
    """
    Prints activation guide (cross-platform safe)
    """

    print("\n📌 Activate environment with:")

    if platform.system() == "Windows":
        print("conda activate pranomics")
    else:
        print("source activate pranomics")


# =====================================================
# MAIN BOOTSTRAP ENTRY
# =====================================================
def bootstrap_conda(env_file=None):
    """
    Full automatic bootstrap pipeline
    """

    wait_for_internet()

    conda_path = find_conda()

    if not conda_path:
        print("\n❌ Conda not found. Installing Miniconda...")
        install_miniconda()

        # refresh PATH after install
        conda_path = str(Path.home() / "miniconda3/bin/conda")

    configure_conda(conda_path)
    create_env(conda_path, env_file)

    activation_instructions()

    print("\n✔ Bootstrap complete")
    