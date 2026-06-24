import os
import pandas as pd
import plotly.express as px


def create_interactive_volcano(gene_map=None):

    os.makedirs("report/interactive", exist_ok=True)

    df = pd.read_csv("DEG/DE_results.csv", index_col=0)
    df["FDR"] = df["FDR"].fillna(1)
    df["-log10FDR"] = -1 * df["FDR"].apply(lambda x: max(x, 1e-300))

    # 🧬 annotation
    if gene_map:
        df["gene_name"] = df.index.map(lambda x: gene_map.get(x, x))
    else:
        df["gene_name"] = df.index

    df["status"] = "Not Significant"
    df.loc[(df["FDR"] < 0.05) & (df["logFC"] > 1), "status"] = "Up"
    df.loc[(df["FDR"] < 0.05) & (df["logFC"] < -1), "status"] = "Down"

    fig = px.scatter(
        df,
        x="logFC",
        y="-log10FDR",
        color="status",
        hover_name="gene_name",
        custom_data=["gene_name", "logFC", "FDR"],
        title="Interactive Volcano Plot"
    )
    fig.update_traces(  
    customdata=df[["gene_name", "logFC", "FDR", "status"]],
    hovertemplate=
    "<b>%{customdata[0]}</b><br>" +
    "logFC: %{customdata[1]}<br>" +
    "FDR: %{customdata[2]}<br>" +
    "Status: %{customdata[3]}<extra></extra>"
)

    # 🧠 JS click behavior
    fig.update_traces(
        marker=dict(size=8),
        selector=dict(mode="markers")
    )

    fig.update_layout(
        clickmode="event+select"
    )

    output = "report/interactive/volcano.html"
    fig.write_html(output, include_plotlyjs="cdn")

    print("✅ Clickable Volcano created")

    return output
