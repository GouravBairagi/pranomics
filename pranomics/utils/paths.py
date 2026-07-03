from pathlib import Path
import os


class Paths:
    """
    Single unified path manager (NO global constants anymore)
    """

    def __init__(self, base_dir=None):

        env_base = os.getenv("PRANOMICS_BASE_DIR")

        self.base = Path(
            base_dir or env_base or Path.cwd()
        ).resolve()

        # Core directories
        self.data = self.base / "data"
        self.metadata = self.base / "metadata"
        self.reference = self.base / "reference"
        self.counts = self.base / "counts"
        self.deg = self.base / "DEG"
        self.report = self.base / "report"
        self.logs = self.base / "logs"
        self.scripts = self.base / "scripts"

    def create_all(self):
        for p in [
            self.data,
            self.metadata,
            self.reference,
            self.counts,
            self.deg,
            self.report,
            self.logs,
        ]:
            p.mkdir(parents=True, exist_ok=True)

        return self
        