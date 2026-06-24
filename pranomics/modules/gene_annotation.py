import os

import pandas as pd

try:
    import requests
except ImportError:
    requests = None


# -------------------------------
# LAYER 1: LOCAL ANNOTATION FILE
# -------------------------------
def load_local_annotation(file="reference/annotation.csv"):
    if not os.path.exists(file):
        return None
    return pd.read_csv(file)


# -------------------------------
# LAYER 2: ENSEMBL LOOKUP
# -------------------------------
def query_ensembl(gene_id, species="homo_sapiens"):
    if requests is None:
        return None

    try:
        url = f"https://rest.ensembl.org/lookup/symbol/{species}/{gene_id}?content-type=application/json"
        r = requests.get(url, headers={"Content-Type": "application/json"})
        if r.status_code == 200:
            data = r.json()
            return {
                "name": data.get("display_name", gene_id),
                "description": data.get("description", "NA"),
                "source": "Ensembl"
            }
    except:
        pass
    return None


# -------------------------------
# LAYER 3: FALLBACK
# -------------------------------
def fallback_annotation(gene_id):
    return {
        "name": gene_id,
        "description": "No annotation found",
        "source": "fallback"
    }


# -------------------------------
# MAIN FUNCTION
# -------------------------------
def annotate_gene(gene_id, local_db=None, species="homo_sapiens"):

    # 1. local DB check
    if local_db is not None:
        match = local_db[local_db.iloc[:, 0] == gene_id]
        if not match.empty:
            return {
                "name": match.iloc[0].get("gene_name", gene_id),
                "description": match.iloc[0].get("description", ""),
                "source": "local"
            }

    # 2. Ensembl
    result = query_ensembl(gene_id, species=species)
    if result:
        return result

    # 3. fallback
    return fallback_annotation(gene_id)
