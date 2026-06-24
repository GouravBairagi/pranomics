import os
import json

CHECKPOINT_FILE = "report/checkpoints.json"


def load_checkpoint():
    if not os.path.exists(CHECKPOINT_FILE):
        return {}

    try:
        with open(CHECKPOINT_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_checkpoint(data):
    os.makedirs("report", exist_ok=True)

    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def mark_done(sample, step):
    data = load_checkpoint()

    if sample not in data:
        data[sample] = []

    if step not in data[sample]:
        data[sample].append(step)

    save_checkpoint(data)


def is_done(sample, step):
    data = load_checkpoint()
    return step in data.get(sample, [])
