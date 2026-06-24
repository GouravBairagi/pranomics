import glob
import os


# -----------------------------
# FIND REFERENCE GENOME
# -----------------------------
def get_reference_fasta(reference_dir="reference"):

    fasta_files = (
        glob.glob(f"{reference_dir}/*.fna") +
        glob.glob(f"{reference_dir}/*.fa") +
        glob.glob(f"{reference_dir}/*.fasta")
    )

    if not fasta_files:
        raise FileNotFoundError(
            "❌ No reference FASTA found in reference/"
        )

    print(f"🧬 Reference genome: {fasta_files[0]}")
    return fasta_files[0]


# -----------------------------
# FIND GFF FILE
# -----------------------------
def get_gff_file(reference_dir="reference"):

    gff_files = glob.glob(f"{reference_dir}/*.gff") + glob.glob(f"{reference_dir}/*.gtf")

    if not gff_files:
        raise FileNotFoundError(
            "❌ No GFF/GTF file found in reference/"
        )

    print(f"📄 Annotation file: {gff_files[0]}")
    return gff_files[0]


# -----------------------------
# VALIDATE REFERENCE SETUP
# -----------------------------
def validate_reference(reference_dir="reference"):

    print("\n🧬 VALIDATING REFERENCE...\n")

    fasta = get_reference_fasta(reference_dir)
    gff = get_gff_file(reference_dir)

    return fasta, gff
