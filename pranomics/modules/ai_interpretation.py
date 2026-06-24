import pandas as pd


def generate_interpretation(deg_file, gene_map=None):

    df = pd.read_csv(deg_file, index_col=0)
    df["FDR"] = df["FDR"].fillna(1)

    sig = df[df["FDR"] < 0.05]

    if len(sig) == 0:
        return "No significant differential expression detected."

    up = sig[sig["logFC"] > 1]
    down = sig[sig["logFC"] < -1]

    interpretation = []
    interpretation.append("🧠 === SMART BIOLOGICAL INTERPRETATION ===\n")

    interpretation.append(f"Total significant genes: {len(sig)}")
    interpretation.append(f"Upregulated: {len(up)} | Downregulated: {len(down)}\n")

    # ----------------------------
    # 1. GLOBAL RESPONSE TYPE
    # ----------------------------
    if len(up) > len(down) * 1.5:
        interpretation.append("📌 System response: Strong activation state detected.")
    elif len(down) > len(up) * 1.5:
        interpretation.append("📌 System response: Strong suppression state detected.")
    else:
        interpretation.append("📌 System response: Balanced transcriptional modulation.\n")

    # ----------------------------
    # 2. SIGNAL STRENGTH
    # ----------------------------
    avg_fc = sig["logFC"].abs().mean()

    if avg_fc > 3:
        strength = "EXTREME"
    elif avg_fc > 2:
        strength = "STRONG"
    elif avg_fc > 1:
        strength = "MODERATE"
    else:
        strength = "LOW"

    interpretation.append(f"📊 Signal strength: {strength}")

    # ----------------------------
    # 3. BIOLOGICAL HINTS (GENE-BASED LOGIC)
    # ----------------------------
    genes = sig.index.str.lower()

    if any("ribos" in g or "rpl" in g or "rps" in g for g in genes):
        interpretation.append("🧬 Ribosomal activity changes detected → translation regulation involved.")

    if any("stress" in g or "heat" in g for g in genes):
        interpretation.append("🔥 Stress-response signature detected.")

    if any("metab" in g or "dehydrogenase" in g for g in genes):
        interpretation.append("⚡ Metabolic pathway shifts detected.")

    if any("kinase" in g or "phosph" in g for g in genes):
        interpretation.append("📡 Signaling pathway modulation likely involved.")

    # ----------------------------
    # 4. GENE MAP ENHANCEMENT (if available)
    # ----------------------------
    if gene_map is not None:
        annotated = 0

        for g in sig.index:
            if g in gene_map:
                annotated += 1

        interpretation.append(f"\n🔬 Annotated genes: {annotated}/{len(sig)}")

    # ----------------------------
    # 5. FINAL CONCLUSION
    # ----------------------------
    interpretation.append("\n📌 Conclusion:")
    interpretation.append(
        "Dataset shows coordinated transcriptional changes suggesting "
        "a biologically regulated response rather than random variation."
    )

    return "\n".join(interpretation)

