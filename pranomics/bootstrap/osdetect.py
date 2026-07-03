import platform
import os


# =====================================================
# SYSTEM INFORMATION
# =====================================================
def get_system_info():
    """
    Returns complete system information dictionary
    """
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine().lower(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }


# =====================================================
# OS CHECKS
# =====================================================
def is_windows():
    return platform.system().lower() == "windows"


def is_linux():
    return platform.system().lower() == "linux"


def is_macos():
    return platform.system().lower() == "darwin"


# =====================================================
# ARCHITECTURE NORMALIZATION
# =====================================================
def get_architecture():
    """
    Normalizes architecture names across systems
    """

    machine = platform.machine().lower()

    if machine in ("x86_64", "amd64"):
        return "x86_64"

    if machine in ("arm64", "aarch64"):
        return "arm64"

    if "arm" in machine:
        return "arm"

    return machine


# =====================================================
# ENVIRONMENT CHECKS
# =====================================================
def is_admin():
    """
    Checks if running as admin/root
    """
    try:
        return os.geteuid() == 0
    except AttributeError:
        # Windows fallback
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


def get_home():
    return os.path.expanduser("~")
    