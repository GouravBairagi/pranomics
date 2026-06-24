import os
import pandas as pd
import base64


# -----------------------------
# SAFE IMAGE LOADER
# -----------------------------
def img_to_base64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()


# -----------------------------
# MAIN REPORT GENERATOR
# -----------------------------
def generate_html_report(ai_text):

    os.makedirs("report", exist_ok=True)

    deg_file = "DEG/DE_results.csv"
    summary_file = "DEG/final_report.txt"

    # Images
    pca_img = "DEG/pca.png"
    heatmap_img = "DEG/heatmap.png"

    # Volcano is HTML now (IMPORTANT FIX)
    volcano_html = "report/interactive/volcano.html"

    output_file = "report/pranomics_Report.html"

    print("\n📄 Generating FULL HTML report (PRO VERSION)...")

    # -----------------------------
    # Load DEG table safely
    # -----------------------------
    if not os.path.exists(deg_file):
        raise FileNotFoundError("DEG results not found")

    df = pd.read_csv(deg_file, index_col=0)
    df["FDR"] = df["FDR"].fillna(1)

    up = df[(df["FDR"] < 0.05) & (df["logFC"] > 1)]
    down = df[(df["FDR"] < 0.05) & (df["logFC"] < -1)]

    # -----------------------------
    # Pipeline summary
    # -----------------------------
    summary_text = ""
    if os.path.exists(summary_file):
        with open(summary_file, "r") as f:
            summary_text = f.read()

    # -----------------------------
    # Convert images safely
    # -----------------------------
    pca_b64 = img_to_base64(pca_img)
    heatmap_b64 = img_to_base64(heatmap_img)

    # -----------------------------
    # HTML BUILD
    # -----------------------------
    html = f"""
    <html>
    <head>
        <title>RNA-seq Report</title>

        <style>
            body {{
                font-family: Arial;
                margin: 0;
                background: #f4f6f9;
            }}

            .header {{
                background: #2c3e50;
                color: white;
                padding: 20px;
                text-align: center;
            }}

            .container {{
                padding: 20px;
            }}

            .box {{
                background: white;
                padding: 20px;
                margin: 20px 0;
                border-radius: 12px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            }}

            img {{
                max-width: 100%;
                border-radius: 8px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
            }}

            th {{
                background: #34495e;
                color: white;
                padding: 8px;
            }}

            td {{
                padding: 6px;
                border: 1px solid #ddd;
            }}
        </style>
    </head>

    <body>

    <div class="header">
        <h1>🧬 RNA-seq Analysis Report</h1>
        <p>Automated Bioinformatics Pipeline</p>
    </div>

    <div class="container">

        <div class="box">
            <h2>📊 Summary</h2>
            <p><b>Total genes:</b> {len(df)}</p>
            <p><b>Upregulated:</b> {len(up)}</p>
            <p><b>Downregulated:</b> {len(down)}</p>
        </div>

        <div class="box">
            <h2>📄 Pipeline Summary</h2>
            <pre>{summary_text}</pre>
        </div>
    """

    # -----------------------------
    # PCA (safe)
    # -----------------------------
    if pca_b64:
        html += f"""
        <div class="box">
            <h2>📌 PCA Plot</h2>
            <img src="data:image/png;base64,{pca_b64}">
        </div>
        """

    # -----------------------------
    # Volcano (HTML iframe FIX)
    # -----------------------------
    if os.path.exists(volcano_html):
        html += f"""
        <div class="box">
            <h2>🌋 Volcano Plot (Interactive)</h2>
            <iframe src="interactive/volcano.html"
                    width="100%"
                    height="600px"
                    style="border:none;border-radius:10px;">
            </iframe>
        </div>
        """

    # -----------------------------
    # Heatmap (safe)
    # -----------------------------
    if heatmap_b64:
        html += f"""
        <div class="box">
            <h2>🧊 Heatmap</h2>
            <img src="data:image/png;base64,{heatmap_b64}">
        </div>
        """

    # -----------------------------
    # Tables
    # -----------------------------
    html += f"""
        <div class="box">
            <h2>🔥 Top Upregulated Genes</h2>
            {up.sort_values("logFC", ascending=False).head(10).to_html(index=True)}
        </div>

        <div class="box">
            <h2>❄ Top Downregulated Genes</h2>
            {down.sort_values("logFC").head(10).to_html(index=True)}
        </div>

        <div class="box">
            <h2>🧠 Interpretation</h2>
            <pre style="white-space: pre-wrap;">{ai_text}</pre>
        </div>

    </div>
    </body>
    </html>
    """

    with open(output_file, "w") as f:
        f.write(html)

    print("✅ PRO REPORT GENERATED → report/pranomics_Report.html")
    
