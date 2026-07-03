import os
import shutil
import subprocess
import platform
import urllib.request


# --------------------------------------------------
# FIND EXISTING CONDA
# --------------------------------------------------
def _find_conda():
    conda = shutil.which("conda")
    if conda:
        return conda

    paths = [
        os.path.expanduser("~/miniconda3/bin/conda"),
        os.path.expanduser("~/anaconda3/bin/conda"),
        "/opt/miniconda3/bin/conda",
        "/opt/anaconda3/bin/conda",
    ]

    # Windows
    if platform.system() == "Windows":
        paths.extend([
            os.path.expanduser("~/miniconda3/Scripts/conda.exe"),
            os.path.expanduser("~/Anaconda3/Scripts/conda.exe"),
        ])

    for p in paths:
        if os.path.exists(p):
            return p

    return None


# --------------------------------------------------
# DOWNLOAD MINICONDA
# --------------------------------------------------
def _download_miniconda():

    system = platform.system()

    if system == "Linux":
        url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
        installer = "/tmp/miniconda.sh"

    elif system == "Darwin":
        url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
        installer = "/tmp/miniconda.sh"

    elif system == "Windows":
        url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"
        installer = os.path.join(os.environ["TEMP"], "miniconda.exe")

    else:
        raise RuntimeError(f"Unsupported OS: {system}")

    print("\n📥 Downloading Miniconda...")

    urllib.request.urlretrieve(url, installer)

    return installer


# --------------------------------------------------
# INSTALL MINICONDA
# --------------------------------------------------
def _install_miniconda():

    installer = _download_miniconda()

    system = platform.system()

    print("⚙ Installing Miniconda...")

    if system in ("Linux", "Darwin"):

        subprocess.run([
            "bash",
            installer,
            "-b",
            "-p",
            os.path.expanduser("~/miniconda3")
        ], check=True)

    elif system == "Windows":

        subprocess.run([
            installer,
            "/InstallationType=JustMe",
            "/RegisterPython=0",
            "/S",
            "/D=" + os.path.expanduser("~/miniconda3")
        ], check=True)

    print("✔ Miniconda installed")


# --------------------------------------------------
# CONFIGURE CONDA
# --------------------------------------------------
def _configure_conda(conda):

    print("\n🔧 Configuring Conda...")

    commands = [

        [conda, "tos", "accept",
         "--override-channels",
         "--channel",
         "https://repo.anaconda.com/pkgs/main"],

        [conda, "tos", "accept",
         "--override-channels",
         "--channel",
         "https://repo.anaconda.com/pkgs/r"],

        [conda, "config", "--add", "channels", "conda-forge"],

        [conda, "config", "--add", "channels", "bioconda"],

        [conda, "config", "--set", "channel_priority", "strict"],
    ]

    for cmd in commands:
        try:
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            pass

    print("✔ Conda configured")


# --------------------------------------------------
# MAIN ENTRY
# --------------------------------------------------
def ensure_conda(skip_install=False):

    conda = _find_conda()

    if not conda:

        print("\n⚠ Conda not detected.")

        if skip_install:
            raise RuntimeError("Conda missing.")

        _install_miniconda()

        conda = _find_conda()

        if not conda:
            raise RuntimeError("Automatic Conda installation failed.")

    conda_dir = os.path.dirname(conda)

    os.environ["PATH"] = conda_dir + os.pathsep + os.environ["PATH"]

    _configure_conda(conda)

    print(f"\n✔ Conda ready ({conda})")

    return conda
    