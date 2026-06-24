from pathlib import Path

# Always resolve project root dynamically
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
REFERENCE_DIR = PROJECT_ROOT / "reference"
REPORT_DIR = PROJECT_ROOT / "report"
DEG_DIR = PROJECT_ROOT / "DEG"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
