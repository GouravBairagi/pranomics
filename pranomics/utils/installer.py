import shutil
import subprocess
import os


# -----------------------------
# VERIFY TOOL
# -----------------------------
def verify_tool(tool_name):
    return shutil.which(tool_name) is not None


# -----------------------------
# APT INSTALL
# -----------------------------
def install_apt_package(package):
    print(f"\n📦 Installing {package} via apt...")

    subprocess.run(
        ["sudo", "apt", "install", "-y", package],
        check=True,
    )

    return True


# -----------------------------
# CONDA INSTALL (ROBUST)
# -----------------------------
def install_conda_package(package, channels=None):
    channels = channels or ["bioconda", "conda-forge"]

    print(f"\n📦 Installing {package} via conda...")

    conda_exec = shutil.which("conda")

    # fallback search
    if not conda_exec:
        possible_paths = [
            os.path.expanduser("~/miniconda3/bin/conda"),
            os.path.expanduser("~/anaconda3/bin/conda"),
            "/opt/miniconda3/bin/conda",
            "/opt/anaconda3/bin/conda",
        ]

        for p in possible_paths:
            if os.path.exists(p):
                conda_exec = p
                break

    if not conda_exec:
        raise RuntimeError("Conda not found. Install Miniconda first.")

    cmd = [conda_exec, "install", "-y"]

    for ch in channels:
        cmd += ["-c", ch]

    cmd.append(package)

    subprocess.run(cmd, check=True)

    return True


# -----------------------------
# R PACKAGE INSTALL
# -----------------------------
def install_r_package(package):
    print(f"\n📦 Installing R package: {package}")

    r_command = (
        'if(!requireNamespace("BiocManager", quietly=TRUE)) '
        'install.packages("BiocManager", repos="https://cloud.r-project.org"); '
        f'if(!requireNamespace("{package}", quietly=TRUE)) '
        f'BiocManager::install("{package}", ask=FALSE, update=FALSE)'
    )

    subprocess.run(["Rscript", "-e", r_command], check=True)

    return True
