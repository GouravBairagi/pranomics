from pranomics.utils.paths import DEG_DIR, REPORT_DIR
import pandas as pd
import plotly.express as px
import os


def run_volcano(gene_map=None):

    REPORT_DIR.mkdir(exist_ok=True, parents=True)

    df = pd.read_csv("DEG/DE_results.csv", index_col=0)
    df["FDR"] = df["FDR"].fillna(1)

    df["-log10FDR"] = -1 * df["FDR"].apply(lambda x: max(x, 1e-300))

    df["gene_name"] = df.index.map(lambda x: gene_map.get(x, x)) if gene_map else df.index

    df["status"] = "Not Significant"
    df.loc[(df["FDR"] < 0.05) & (df["logFC"] > 1), "status"] = "Up"
    df.loc[(df["FDR"] < 0.05) & (df["logFC"] < -1), "status"] = "Down"

    fig = px.scatter(
        df,
        x="logFC",
        y="-log10FDR",
        color="status",
        hover_name="gene_name",
        title="Volcano Plot"
    )

    output = REPORT_DIR / "interactive" / "volcano.html"
    output.parent.mkdir(parents=True, exist_ok=True)

    fig.write_html(str(output))

    return str(output)

