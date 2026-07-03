import os
import pandas as pd



def generate_deg_tables():

    os.makedirs("DEG", exist_ok=True)

    input_file = "DEG/DE_results.csv"

    up_file = "DEG/upregulated.csv"
    down_file = "DEG/downregulated.csv"

    if os.path.exists(up_file) and os.path.exists(down_file):
        print("✓ DEG tables are already generated.")
        return

    print("\n📊 DEG tables are being generated.")

    df = pd.read_csv(input_file, index_col=0)

    # Clean FDR (important safety step)
    df["FDR"] = df["FDR"].fillna(1)

    # Upregulated genes
    up = df[(df["FDR"] < 0.05) & (df["logFC"] > 1)]

    # Downregulated genes
    down = df[(df["FDR"] < 0.05) & (df["logFC"] < -1)]

    up.to_csv(up_file)
    down.to_csv(down_file)

    print(f"✅ Upregulated genes identified: {len(up)}")
    print(f"✅ Downregulated genes identified: {len(down)}")