"""Build PadChest-Effusion from a local copy of PadChest and the shipped split file.

Labels are recomputed from the official PadChest CSV with the rules below; images are converted once from 16-bit PNG
to 8-bit grayscale (longest side 512).
  y       'pleural effusion' in Labels
  view    Projection PA -> 0, AP / AP_horizontal -> 1
  device  any support-device label (DEVICES below)
Images whose labels include a chest drain, 'exclude' or 'suboptimal study' were excluded when the split was made.

  PADCHEST_DIR=/path/to/padchest python experiments/00_build_benchmark.py
"""
import argparse
import ast
import csv
import json
import os
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from truesign import paths  # noqa: E402
from truesign.data import CLASS_NAMES, GROUP_NAMES  # noqa: E402

TARGET = "pleural effusion"
DEVICES = {"NSG tube", "endotracheal tube", "tracheostomy tube", "central venous catheter",
           "central venous catheter via jugular vein", "central venous catheter via subclavian vein",
           "central venous catheter via umbilical vein", "reservoir central venous catheter", "catheter",
           "pacemaker", "dual chamber device", "single chamber device", "electrical device", "gastrostomy tube",
           "nephrostomy tube", "ventriculoperitoneal drain tube"}


def parse(x):
    try:
        return [s.strip() for s in ast.literal_eval(x)] if isinstance(x, str) else []
    except (ValueError, SyntaxError):
        return []


def convert(job):
    src, dst = job
    if os.path.exists(dst):
        return
    a = np.asarray(Image.open(src))
    if a.dtype != np.uint8:  # 16-bit MONOCHROME2 PNG stored on the full 16-bit range
        a = (a.astype(np.float32) / 65535.0 * 255.0).clip(0, 255).astype(np.uint8)
    im = Image.fromarray(a, mode="L")
    im.thumbnail((512, 512), Image.BICUBIC)
    im.save(dst)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=16)
    args = ap.parse_args()
    split = {r["ImageID"]: int(r["split"]) for r in csv.DictReader(open(paths.SPLIT_FILE))}
    df = pd.read_csv(os.path.join(paths.PADCHEST_DIR, paths.PADCHEST_CSV), low_memory=False)
    df = df[df.ImageID.isin(split)].copy()
    if len(df) != len(split):
        raise SystemExit(f"{len(split) - len(df)} split images not found in the PadChest CSV")
    df["L"] = df.Labels.map(parse)
    df["y"] = df.L.map(lambda L: int(TARGET in L))
    df["view"] = df.Projection.isin(["AP", "AP_horizontal"]).astype(int)
    df["device"] = df.L.map(lambda L: int(bool(set(L) & DEVICES)))
    df["group"] = 2 * df.view + df.device
    df["split"] = df.ImageID.map(split)

    os.makedirs(os.path.join(paths.DATA_DIR, "images"), exist_ok=True)
    jobs = [(os.path.join(paths.PADCHEST_DIR, f), os.path.join(paths.DATA_DIR, "images", f)) for f in df.ImageID]
    with ProcessPoolExecutor(args.workers) as ex:
        list(ex.map(convert, jobs, chunksize=16))

    out = os.path.join(paths.DATA_DIR, "metadata.csv")
    df.assign(img_filename="images/" + df.ImageID)[["img_filename", "y", "view", "device", "group", "split"]].to_csv(
        out, index=False)
    counts = {s: {f"{CLASS_NAMES[y]}|{GROUP_NAMES[g]}": n for (y, g), n in
                  sorted(Counter(zip(d.y, d.group)).items())} for s, d in df.groupby("split")}
    print(json.dumps({"train/val/test": {str(k): v for k, v in counts.items()}}, indent=1))
    print("wrote", out)


if __name__ == "__main__":
    main()
