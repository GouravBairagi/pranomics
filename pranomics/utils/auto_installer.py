import time
import subprocess
import shutil

from pranomics.utils.installer import (
    install_apt_package,
    install_conda_package,
    install_r_package,
    verify_tool,
)


# -----------------------------
# TOOL MAP
# -----------------------------
TOOL_MAP = {
    "fastq-dump": ("conda", "sra-tools"),
    "fastqc": ("conda", "fastqc"),
    "bowtie2": ("conda", "bowtie2"),
    "bowtie2-build": ("conda", "bowtie2"),
    "samtools": ("conda", "samtools"),
    "stringtie": ("conda", "stringtie"),
    "java": ("apt", "default-jre"),
    "Rscript": ("conda", "r-base"),

    # IMPORTANT
    "trimmomatic": ("conda", "trimmomatic"),
}


# -----------------------------
# CONDA CHECK
# -----------------------------
def _conda_available():
    return shutil.which("conda") is not None


# -----------------------------
# SAFE INSTALL TOOL
# -----------------------------
def install_tool(tool, retries=2):
    method, package = TOOL_MAP.get(tool, ("conda", tool))

    print(f"\n🔧 Installing tool: {tool}")
    print(f"📦 Method: {method} | Package: {package}")

    for attempt in range(1, retries + 1):

        try:
            if method == "apt":
                install_apt_package(package)

            elif method == "conda":
                if not _conda_available():
                    raise RuntimeError("conda not available in PATH")

                install_conda_package(package)

            else:
                raise RuntimeError(f"Unknown method: {method}")

            if verify_tool(tool):
                print(f"✔ {tool} installed successfully")
                return True

        except Exception as e:
            print(f"❌ Attempt {attempt} failed for {tool}: {e}")
            time.sleep(2 * attempt)

    print(f"❌ FINAL FAILURE: {tool}")
    return False


# -----------------------------
# R PACKAGE INSTALL
# -----------------------------
def install_r_pkg(package):
    print(f"\n🔧 Installing R package: {package}")

    try:
        install_r_package(package)
        return True
    except Exception as e:
        print(f"❌ R install failed: {package} -> {e}")
        return False


# -----------------------------
# MAIN INSTALL LOOP
# -----------------------------
def install_missing(report):
    missing_tools = report.get("missing_tools", [])
    missing_r = report.get("missing_r_packages", [])

    print("\n==============================")
    print("🚀 AUTO INSTALLATION STARTING")
    print("==============================")

    # install tools
    for tool in missing_tools:
        ok = install_tool(tool)
        if not ok:
            print(f"❌ FAILED: {tool}")

    # install R packages
    for pkg in missing_r:
        ok = install_r_pkg(pkg)
        if not ok:
            print(f"❌ FAILED R: {pkg}")

    print("\n==============================")
    print("🏁 INSTALLATION COMPLETE")
    print("==============================")
    
