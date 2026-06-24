import pandas as pd
import re


def parse_gff_attributes(attr_string):
    """
    Extract key=value pairs from GFF/GTF attribute column
    """
    attrs = {}

    # split by semicolon
    parts = attr_string.strip().split(";")

    for p in parts:
        if "=" in p:
            k, v = p.split("=", 1)
        elif " " in p:
            k, v = p.split(" ", 1)
        else:
            continue

        attrs[k.strip()] = v.strip().replace('"', '')

    return attrs


def build_gene_annotation(gff_file):

    print("🧬 Building gene annotation database from GFF...")

    gene_map = {}

    with open(gff_file, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue

            cols = line.strip().split("\t")
            if len(cols) < 9:
                continue

            feature_type = cols[2]
            attributes = cols[8]

            if feature_type.lower() in ["gene", "mrna", "transcript"]:

                attrs = parse_gff_attributes(attributes)

                gene_id = attrs.get("gene_id") or attrs.get("ID")
                gene_name = attrs.get("gene_name") or attrs.get("Name") or gene_id
                product = attrs.get("product") or attrs.get("description") or "NA"

                if gene_id:
                    gene_map[gene_id] = {
                        "gene_name": gene_name,
                        "description": product
                    }

    print(f"✅ Annotation built for {len(gene_map)} genes")

    return gene_map


def annotate_gene(gene_id, gene_map):

    if gene_id in gene_map:
        return gene_map[gene_id]

    return {
        "gene_name": gene_id,
        "description": "No annotation found"
    }