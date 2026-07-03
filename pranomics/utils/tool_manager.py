import shutil
import subprocess
import time
from pranomics.utils.conda_bootstrap import ensure_conda

# =====================================================
# TOOL REGISTRY (SOURCE OF TRUTH)
# =====================================================
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


# =====================================================
# CHECK TOOL
# =====================================================
def is_tool_available(tool: str) -> bool:
    return shutil.which(tool) is not None


def conda_available():
    return shutil.which("conda") is not None


# =====================================================
# INSTALL DISPATCHERS
# =====================================================
def install_conda(pkg):

    conda = ensure_conda()

    subprocess.run(
        [
            conda,
            "install",
            "-y",
            "-c",
            "bioconda",
            "-c",
            "conda-forge",
            pkg,
        ],
        check=True,
    )
    


def install_apt(pkg):
    subprocess.run(["sudo", "apt", "install", "-y", pkg], check=True)


def install_r(pkg):
    r_cmd = (
        'if(!requireNamespace("BiocManager", quietly=TRUE)) '
        'install.packages("BiocManager", repos="https://cloud.r-project.org"); '
        f'if(!requireNamespace("{pkg}", quietly=TRUE)) '
        f'BiocManager::install("{pkg}", ask=FALSE, update=FALSE)'
    )
    subprocess.run(["Rscript", "-e", r_cmd], check=True)


# =====================================================
# SINGLE TOOL INSTALL
# =====================================================
def install_tool(tool: str, retries=2):

    # clean bypass list (IMPORTANT FIX)
    NON_INSTALLABLE = {
        "python_version",
        "python",
        "pip",
    }

    if tool in NON_INSTALLABLE:
        print(f"✔ Skipping system check: {tool}")
        return True

    if tool not in TOOL_REGISTRY:
        print(f"⚠ Unknown tool: {tool} (skipping)")
        return False

    meta = TOOL_REGISTRY[tool]
    ttype = meta["type"]
    pkg = meta["pkg"]

    print(f"\n🔧 Installing {tool} → {pkg} ({ttype})")

    for attempt in range(1, retries + 1):
        try:
            if ttype == "conda":
                install_conda(pkg)
            elif ttype == "apt":
                install_apt(pkg)
            elif ttype == "r":
                install_r(pkg)
            else:
                raise ValueError(f"Unknown install type: {ttype}")

            if is_tool_available(tool):
                print(f"✔ Installed: {tool}")
                return True

        except Exception as e:
            print(f"❌ Attempt {attempt} failed for {tool}: {e}")
            time.sleep(2 * attempt)

    print(f"❌ FAILED: {tool}")
    return False


# =====================================================
# INSTALL MISSING TOOLS
# =====================================================
def install_missing(report: dict):

    tools = report.get("missing_tools", [])

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
    