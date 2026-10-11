"""PadChest-Effusion benchmark metadata.

benchmark/padchest_effusion_split.csv (shipped) holds only PadChest ImageIDs and their split, because the PadChest
research-use agreement does not allow redistributing its labels or images. experiments/build_benchmark.py recomputes all
labels from the user's own copy of the PadChest CSV and writes <TRUESIGN_DATA_DIR>/metadata.csv, one row per image:
  img_filename   path under the benchmark image directory
  y              0 no pleural effusion, 1 pleural effusion
  view           0 PA (standing), 1 AP / AP_horizontal (bedside)
  device         0 no support device, 1 support device (tubes, lines, catheters, pacemakers)
  group          2 * view + device (the spurious attribute; 4 values -> 8 (y, group) cells)
  split          0 train (correlated), 1 val (balanced), 2 test (balanced)
"""
import csv
import os

import numpy as np

from . import paths

CLASS_NAMES = ["no_effusion", "effusion"]
GROUP_NAMES = ["PA+no_device", "PA+device", "AP+no_device", "AP+device"]
SPLITS = {"train": 0, "val": 1, "test": 2}


def load_metadata(path=None):
    path = path or os.path.join(paths.DATA_DIR, "metadata.csv")
    rows = list(csv.DictReader(open(path)))
    return {
        "files": [r["img_filename"] for r in rows],
        "y": np.array([int(r["y"]) for r in rows]),
        "group": np.array([int(r["group"]) for r in rows]),
        "view": np.array([int(r["view"]) for r in rows]),
        "device": np.array([int(r["device"]) for r in rows]),
        "split": np.array([int(r["split"]) for r in rows]),
    }
