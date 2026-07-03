import importlib
import subprocess
import sys
import os
import pandas as pd

from pranomics.utils.tool_manager import (
    TOOL_REGISTRY,
    is_tool_available,
)

# -----------------------------
# PYTHON DEPENDENCIES
# -----------------------------

PYTHON_PACKAGES = [
    "pandas",
    "numpy",
    "matplotlib",
    "plotly",
    "rich",
]

# -----------------------------
# R PACKAGES
# -----------------------------

REQUIRED_R_PACKAGES = [
    "edgeR",
    "limma",
]


# -----------------------------
# PYTHON CHECK
# -----------------------------

def check_python():
    v = sys.version_info

    if v < (3, 10):
        raise RuntimeError(
            f"Python 3.10+ required, found {v.major}.{v.minor}"
        )

    return f"{v.major}.{v.minor}"


def check_python_package(pkg):
    try:
        importlib.import_module(pkg)
        return True
    except ImportError:
        return False


# -----------------------------
# TOOL CHECK
# -----------------------------

def check_tools():

    status = {}
    missing = []

    for tool in TOOL_REGISTRY.keys():

        if is_tool_available(tool):
            status[tool] = "found"
        else:
            status[tool] = "missing"
            missing.append(tool)

    return status, missing


# -----------------------------
# R PACKAGE CHECK
# -----------------------------

def check_r_packages():

    if not is_tool_available("Rscript"):
        return REQUIRED_R_PACKAGES

    missing = []

    for pkg in REQUIRED_R_PACKAGES:

        cmd = [
            "Rscript",
            "-e",
            f'if(!requireNamespace("{pkg}", quietly=TRUE)) quit(status=1)'
        ]

        result = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if result.returncode != 0:
            missing.append(pkg)

    return missing


# -----------------------------
# METADATA HELPERS
# -----------------------------

def _guess_column(columns, keywords):

    for col in columns:

        lower = col.lower()

        if any(k in lower for k in keywords):
            return col

    return None


# -----------------------------
# METADATA VALIDATION
# -----------------------------

def validate_metadata(
    metadata,
    samples,
    sample_col=None,
    condition_col=None,
):

    if not os.path.exists(metadata):
        raise FileNotFoundError(
            f"Metadata file not found: {metadata}"
        )

    df = pd.read_csv(metadata)

    columns = list(df.columns)

    print(f"\n📄 Metadata columns detected: {columns}")

    # -----------------------------
    # Sample Column
    # -----------------------------

    if not sample_col or sample_col not in df.columns:

        sample_col = _guess_column(
            columns,
            ["sample", "id", "run", "srr"]
        )

    if not sample_col:
        raise ValueError(
            f"Could not detect sample column. Available columns: {columns}"
        )

    # -----------------------------
    # Condition Column
    # -----------------------------

    if not condition_col or condition_col not in df.columns:

        condition_col = _guess_column(
            columns,
            [
                "condition",
                "group",
                "treatment",
                "status",
                "class",
            ],
        )

    if not condition_col:
        raise ValueError(
            f"Could not detect condition column. Available columns: {columns}"
        )

    print(f"✔ Using sample column: {sample_col}")
    print(f"✔ Using condition column: {condition_col}")

    # -----------------------------
    # Sample Matching
    # -----------------------------

    metadata_samples = set(
        df[sample_col].astype(str)
    )

    input_samples = set(
        map(str, samples)
    )

    missing = input_samples - metadata_samples

    if missing:

        raise ValueError(
            f"Samples missing in metadata: {sorted(missing)}"
        )

    print("✔ Metadata validation OK")

    return True


# -----------------------------
# MAIN ENVIRONMENT VALIDATION
# -----------------------------

def validate_environment():

    python_version = check_python()

    missing_python = [
        pkg
        for pkg in PYTHON_PACKAGES
        if not check_python_package(pkg)
    ]

    tool_status, missing_tools = check_tools()

     # safety filter (prevents installer crash)
    missing_tools = [
    t for t in missing_tools
    if t not in ("python_version", "python", "pip")
]

    missing_r = check_r_packages()

    status = (
        "ready"
        if not (
            missing_tools
            or missing_python
            or missing_r
        )
        else "not_ready"
    )

    return {
        "python_version": python_version,
        "tools": tool_status,
        "missing_tools": missing_tools,
        "missing_r_packages": missing_r,
        "missing_python_packages": missing_python,
        "status": status,
    }

