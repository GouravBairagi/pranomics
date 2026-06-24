import os
import json

STATE_DIR = ".pranomics_state"


def _path(step):
    os.makedirs(STATE_DIR, exist_ok=True)
    return os.path.join(STATE_DIR, f"{step}_done.json")


def load_done(step):
    path = _path(step)
    if not os.path.exists(path):
        return set()

    with open(path, "r") as f:
        return set(json.load(f))


def mark_done(step, sample):
    path = _path(step)

    done = load_done(step)
    done.add(sample)

    with open(path, "w") as f:
        json.dump(sorted(list(done)), f, indent=2)


def is_done(step, sample):
    return sample in load_done(step)
