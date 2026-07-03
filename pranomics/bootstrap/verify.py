import os
import subprocess
import sys
from pathlib import Path

from pranomics.bootstrap.osdetect import get_system_info, is_linux
from pranomics.bootstrap.internet import internet_available


# =====================================================
# SYSTEM HEALTH CHECK
# =====================================================
def system_health_check():
    """
    Checks if system is ready for Pranomics installation
    """

    info = get_system_info()

    print("\n🧪 Running system health check...")

    checks = {
        "python_version_ok": _check_python_version(),
        "internet": internet_available(),
        "os_supported": _check_os(),
        "disk_space": _check_disk_space(),
    }

    all_ok = all(checks.values())

    print("\n📊 SYSTEM CHECK SUMMARY")
    for k, v in checks.items():
        status = "✔" if v else "❌"
        print(f"{status} {k}")

    return all_ok, checks


# =====================================================
# PYTHON VERSION CHECK
# =====================================================
def _check_python_version():
    """
    Requires Python >= 3.10 (your project requirement)
    """
    return sys.version_info >= (3, 10)


# =====================================================
# OS SUPPORT CHECK
# =====================================================
def _check_os():
    """
    Currently optimized for Linux (bioinformatics standard)
    """
    return is_linux()


# =====================================================
# DISK SPACE CHECK
# =====================================================
def _check_disk_space(min_gb=5):
    """
    Ensures enough space for:
    - Conda (~3GB)
    - reference genomes
    - intermediate BAM files
    """

    try:
        stat = os.statvfs("/")
        free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
        return free_gb >= min_gb
    except Exception:
        return True  # fallback safe


# =====================================================
# REQUIRED TOOLS CHECK (PRE-CONDA)
# =====================================================
def check_required_system_tools():
    """
    Checks basic system tools required for bootstrap
    """

    tools = ["curl", "wget", "tar"]

    missing = []

    for tool in tools:
        if not subprocess.call(["which", tool],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) == 0:
            missing.append(tool)

    return missing


# =====================================================
# ENVIRONMENT VALIDATION (POST CONDA)
# =====================================================
def validate_bioinformatics_env(tools):
    """
    Validates if required bio tools are installed
    """

    missing = []

    for tool in tools:
        if not subprocess.call(["which", tool],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) == 0:
            missing.append(tool)

    return missing


# =====================================================
# SAFE GUARD FOR PIPELINE START
# =====================================================
def assert_ready():
    """
    Hard stop if system is not ready
    """

    ok, checks = system_health_check()

    if not ok:
        raise RuntimeError(
            f"""
❌ Pranomics system not ready!

Issues detected:
{checks}

👉 Fix environment before running pipeline.
            """
        )

    print("\n✔ System is ready for Pranomics pipeline")
    