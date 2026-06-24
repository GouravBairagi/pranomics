import os
import json
from datetime import datetime
from pranomics.utils.paths import REPORT_DIR


REPORT_DIR.mkdir(exist_ok=True)


class ReportBuilder:

    def __init__(self):
        self.data = {
            "project": "RNA-Seq Analysis Pipeline",
            "created": str(datetime.now()),
            "sections": {}
        }

    def add(self, section, key, value):
        if section not in self.data["sections"]:
            self.data["sections"][section] = {}

        self.data["sections"][section][key] = value

    def save_json(self):
        with open(REPORT_DIR / "report.json", "w") as f:
            json.dump(self.data, f, indent=4)

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

        with open(REPORT_DIR / "index.html", "w") as f:
            f.write(html)
            