import platform


def get_system():

    return {
        "os": platform.system(),
        "machine": platform.machine().lower(),
        "processor": platform.processor(),
        "python": platform.python_version(),
    }


def is_windows():
    return platform.system() == "Windows"


def is_linux():
    return platform.system() == "Linux"


def is_macos():
    return platform.system() == "Darwin"


def architecture():

    machine = platform.machine().lower()

    if machine in ("x86_64", "amd64"):
        return "x86_64"

    if machine in ("arm64", "aarch64"):
        return "arm64"

    return machine
    