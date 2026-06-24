import shutil
import subprocess
import time
import os


# -----------------------------
# TOOL REGISTRY (SOURCE OF TRUTH)
# -----------------------------
TOOL_REGISTRY = {
    "fastq-dump": {"type": "conda", "pkg": "sra-tools"},
    "fastqc": {"type": "conda", "pkg": "fastqc"},
    "bowtie2": {"type": "conda", "pkg": "bowtie2"},
    "bowtie2-build": {"type": "conda", "pkg": "bowtie2"},
    "samtools": {"type": "conda", "pkg": "samtools"},
    "stringtie": {"type": "conda", "pkg": "stringtie"},
    "trimmomatic": {"type": "conda", "pkg": "trimmomatic"},
    "java": {"type": "apt", "pkg": "default-jre"},
    "Rscript": {"type": "conda", "pkg": "r-base"},
}


# -----------------------------
# CHECK TOOL
# -----------------------------
def is_tool_available(tool: str) -> bool:
    return shutil.which(tool) is not None


# -----------------------------
# CONDA CHECK
# -----------------------------
def conda_available():
    return shutil.which("conda") is not None


# -----------------------------
# INSTALL HELPERS
# -----------------------------
def install_conda(pkg):
    if not conda_available():
        raise RuntimeError("Conda not found in PATH")

    cmd = [
        "conda",
        "install",
        "-y",
        "-c", "bioconda",
        "-c", "conda-forge",
        pkg,
    ]
    subprocess.run(cmd, check=True)


def install_apt(pkg):
    cmd = ["sudo", "apt", "install", "-y", pkg]
    subprocess.run(cmd, check=True)


def install_r(pkg):
    r_cmd = (
        'if(!requireNamespace("BiocManager", quietly=TRUE)) '
        'install.packages("BiocManager", repos="https://cloud.r-project.org"); '
        f'if(!requireNamespace("{pkg}", quietly=TRUE)) '
        f'BiocManager::install("{pkg}", ask=FALSE, update=FALSE)'
    )
    subprocess.run(["Rscript", "-e", r_cmd], check=True)


# -----------------------------
# SINGLE INSTALL FUNCTION
# -----------------------------
def install_tool(tool: str, retries=2):

    if tool not in TOOL_REGISTRY:
        raise ValueError(f"Tool not registered: {tool}")

    meta = TOOL_REGISTRY[tool]
    ttype = meta["type"]
    pkg = meta["pkg"]

    print(f"\n🔧 Installing {tool} ({pkg}) via {ttype}")

    for attempt in range(1, retries + 1):
        try:
            if ttype == "conda":
                install_conda(pkg)

            elif ttype == "apt":
                install_apt(pkg)

            elif ttype == "r":
                install_r(pkg)

            else:
                raise ValueError(f"Unknown type: {ttype}")

            if is_tool_available(tool):
                print(f"✔ Installed: {tool}")
                return True

        except Exception as e:
            print(f"❌ Attempt {attempt} failed for {tool}: {e}")
            time.sleep(2 * attempt)

    print(f"❌ FAILED: {tool}")
    return False


# -----------------------------
# INSTALL MISSING TOOLS
# -----------------------------
def install_missing(tools: list):
    print("\n==============================")
    print("🚀 TOOL MANAGER INSTALL START")
    print("==============================")

    failed = []

    for tool in tools:
        ok = install_tool(tool)
        if not ok:
            failed.append(tool)

    print("\n==============================")
    print("🏁 INSTALLATION COMPLETE")
    print("==============================")

    if failed:
        print("❌ Failed tools:", failed)

    return failed
