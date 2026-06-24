import os
import pandas as pd


def generate_deg_summary(gene_map):

    os.makedirs("DEG", exist_ok=True)

    input_file = "DEG/DE_results.csv"
    out_file = "DEG/summary.txt"

    print("\n📄 Generating DEG summary report...")

    df = pd.read_csv(input_file, index_col=0)
    df["FDR"] = df["FDR"].fillna(1)

    total_genes = len(df)

    up = df[(df["FDR"] < 0.05) & (df["logFC"] > 1)]
    down = df[(df["FDR"] < 0.05) & (df["logFC"] < -1)]

    top_up = up.sort_values("logFC", ascending=False).head(5)
    top_down = down.sort_values("logFC").head(5)

    with open(out_file, "w") as f:

        f.write("=== RNA-seq DEG SUMMARY ===\n\n")

        f.write(f"Total genes tested: {total_genes}\n")
        f.write(f"Upregulated genes: {len(up)}\n")
        f.write(f"Downregulated genes: {len(down)}\n\n")

        f.write("=== TOP UPREGULATED ===\n")
        for gene, row in top_up.iterrows():

            info = gene_map.get(gene, {})
            name = info.get("gene_name", gene)
            desc = info.get("description", "NA")

            f.write(
                f"{gene} | {name} | logFC={row['logFC']:.2f} | {desc}\n"
            )

        f.write("\n=== TOP DOWNREGULATED ===\n")
        for gene, row in top_down.iterrows():

            info = gene_map.get(gene, {})
            name = info.get("gene_name", gene)
            desc = info.get("description", "NA")

            f.write(
                f"{gene} | {name} | logFC={row['logFC']:.2f} | {desc}\n"
            )

    print("✅ DEG summary generated → DEG/summary.txt")
    