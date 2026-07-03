import os
import json
from datetime import datetime
from pathlib import Path


class ReportBuilder:

    def __init__(self, base_dir=None):

        # -----------------------------
        # PROJECT ROOT SAFE HANDLING
        # -----------------------------
        self.base = Path(base_dir or os.getcwd()).resolve()
        self.report_dir = self.base / "report"

        self.report_dir.mkdir(parents=True, exist_ok=True)

        self.data = {
            "project": "RNA-Seq Analysis Pipeline",
            "created": str(datetime.now()),
            "sections": {}
        }

    # -----------------------------
    # ADD SECTION DATA
    # -----------------------------
    def add(self, section, key, value):

        if section not in self.data["sections"]:
            self.data["sections"][section] = {}

        self.data["sections"][section][key] = value

    # -----------------------------
    # SAVE JSON
    # -----------------------------
    def save_json(self):

        out_file = self.report_dir / "report.json"

        with open(out_file, "w") as f:
            json.dump(self.data, f, indent=4)

        return str(out_file)

    # -----------------------------
    # BUILD HTML INDEX
    # -----------------------------
    def build_index(self):

        html = f"""
        <html>
        <head>
            <title>{self.data['project']}</title>
            <style>
                body {{ font-family: Arial; margin: 40px; background:#f5f5f5; }}
                .card {{ background:white; padding:20px; margin:10px; border-radius:10px; }}
                h1 {{ color:#2c3e50; }}
                a {{ text-decoration:none; color:#2980b9; }}
            </style>
        </head>
        <body>

        <h1>{self.data['project']}</h1>
        <p>Generated: {self.data['created']}</p>

        <div class="card">
            <h2>Pipeline Sections</h2>
        """

        for sec in self.data["sections"]:
            html += f"<p>📁 {sec}</p>"

        html += """
        </div>
        </body>
        </html>
        """

        index_file = self.report_dir / "index.html"

        with open(index_file, "w") as f:
            f.write(html)

        return str(index_file)
        
