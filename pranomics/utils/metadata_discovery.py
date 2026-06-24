import os


def discover_metadata():

    candidates = [
        "metadata.csv",
        "metadata/metadata.csv",
        "metadata/metadata.csv",
    ]

    for f in candidates:
        if os.path.exists(f):
            print(f"📄 Metadata detected: {f}")
            return f

    raise FileNotFoundError(
        "No metadata file found.\n"
        "Expected:\n"
        "metadata.csv\n"
        "metadata/metadata.csv\n"
        "metadata/metadata.csv"
    )
