import os
import pandas as pd


def generate_final_report():

    os.makedirs("DEG", exist_ok=True)

    input_file = "DEG/DE_results.csv"
    out_file = "DEG/final_report.txt"

    if os.path.exists(out_file):
        print("✓ arrey tension not file bani hui hai ")
        return

    print("\n📄 bs ab rahat ki sans lo ban hi gyi report smjho")

    df = pd.read_csv(input_file, index_col=0)
    df["FDR"] = df["FDR"].fillna(1)

    total = len(df)
    up = df[(df["FDR"] < 0.05) & (df["logFC"] > 1)]
    down = df[(df["FDR"] < 0.05) & (df["logFC"] < -1)]

    top_up = df.sort_values("logFC", ascending=False).head(10)
    top_down = df.sort_values("logFC").head(10)

    with open(out_file, "w") as f:

        f.write("=== RNA-SEQ PIPELINE FINAL REPORT ===\n\n")

        f.write(f"Total genes analyzed: {total}\n")
        f.write(f"Upregulated genes: {len(up)}\n")
        f.write(f"Downregulated genes: {len(down)}\n\n")

        f.write("=== TOP UPREGULATED GENES ===\n")
        for gene, row in top_up.iterrows():
            f.write(f"{gene}\tlogFC={row['logFC']:.2f}\tFDR={row['FDR']:.3f}\n")

        f.write("\n=== TOP DOWNREGULATED GENES ===\n")
        for gene, row in top_down.iterrows():
            f.write(f"{gene}\tlogFC={row['logFC']:.2f}\tFDR={row['FDR']:.3f}\n")

        f.write("\n=== INTERPRETATION ===\n")

        if len(up) == 0 and len(down) == 0:
            f.write("No statistically significant DE genes detected.\n")
            f.write("This may indicate weak biological contrast or limited replicates.\n")
        else:
            f.write("Differential expression detected between conditions.\n")
            f.write("Further pathway analysis recommended.\n")

    print("✅ Lo nipat gya kaam bngyi report")
    