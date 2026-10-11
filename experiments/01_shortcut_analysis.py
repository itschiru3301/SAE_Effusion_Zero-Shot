"""Step 1: does zero-shot CheXzero rely on the view / device shortcuts?

Zero-shot score = cos(image, "Pleural Effusion") - cos(image, "no Pleural Effusion"); prediction = score > 0.
Reported per split (val, test):
  per-group accuracy over the 8 (effusion, view, device) groups, worst-group and overall accuracy
  accuracy when both spurious cues agree with the label vs when both contradict it
  shortcut AUC: within each true class, how well the effusion score separates AP from PA (view) and device from no
  device (device); 0.5 = no shortcut, > 0.5 = the cue raises the effusion score regardless of disease (bootstrap 95 % CI)
  python experiments/01_shortcut_analysis.py --device cuda:0
"""
import argparse
import json
import os
import sys

import numpy as np
import torch.nn.functional as F
from sklearn.metrics import roc_auc_score

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from truesign import paths, prompts  # noqa: E402
from truesign.backbones import load_backbone  # noqa: E402
from truesign.data import SPLITS, load_metadata  # noqa: E402
from truesign.features import image_features  # noqa: E402
from truesign.metrics import bootstrap_ci, group_metrics, within_class_auc  # noqa: E402


def analyse(score, y, view, device, group):
    pred = (score > 0).astype(int)
    r = group_metrics(pred, y, group)
    aligned, conflict = (view == y) & (device == y), (view != y) & (device != y)
    r.update({
        "effusion_auc": float(roc_auc_score(y, score)),
        "acc_cues_agree": float((pred[aligned] == y[aligned]).mean()),
        "acc_cues_contradict": float((pred[conflict] == y[conflict]).mean()),
        "pred_effusion_rate": float(pred.mean()),
    })
    for name, a in (("view", view), ("device", device)):
        r[f"shortcut_auc_{name}"] = within_class_auc(score, y, a)
        r[f"shortcut_auc_{name}_ci"] = bootstrap_ci(lambda i: within_class_auc(score[i], y[i], a[i]), len(y))
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda:0")
    args = ap.parse_args()
    meta = load_metadata()
    bb = load_backbone("chexzero", args.device)
    X = F.normalize(image_features(bb, meta["files"]).to(args.device), dim=-1)
    t = F.normalize(bb.encode_texts(prompts.load("zero_shot")["class prompts"]), dim=-1)   # [no_effusion, effusion]
    score = (X @ t[1] - X @ t[0]).cpu().numpy()
    out = {}
    for split in ("val", "test"):
        m = meta["split"] == SPLITS[split]
        out[split] = analyse(score[m], meta["y"][m], meta["view"][m], meta["device"][m], meta["group"][m])
    os.makedirs(paths.RESULTS, exist_ok=True)
    json.dump(out, open(os.path.join(paths.RESULTS, "01_shortcut_analysis.json"), "w"), indent=2)

    lines = ["# Step 1: zero-shot CheXzero shortcut analysis", "",
             "| | val | test |", "|---|---|---|"]
    for k, lab in (("effusion_auc", "Effusion AUC"), ("overall", "Overall accuracy"), ("worst", "Worst-group accuracy"),
                   ("acc_cues_agree", "Accuracy, both cues agree with label"),
                   ("acc_cues_contradict", "Accuracy, both cues contradict label")):
        lines.append(f"| {lab} | {out['val'][k]:.3f} | {out['test'][k]:.3f} |")
    for k, lab in (("view", "Shortcut AUC, view (AP vs PA)"), ("device", "Shortcut AUC, support device")):
        lines.append(f"| {lab} | " + " | ".join(
            f"{out[s][f'shortcut_auc_{k}']:.3f} [{out[s][f'shortcut_auc_{k}_ci'][0]:.2f}, "
            f"{out[s][f'shortcut_auc_{k}_ci'][1]:.2f}]" for s in ("val", "test")) + " |")
    lines += ["", "Per-group accuracy (test)", "", "| Group | Accuracy |", "|---|---|"]
    lines += [f"| {g.replace('|', ', ')} | {v['acc']:.2f} |" for g, v in out["test"]["groups"].items()]
    open(os.path.join(paths.RESULTS, "01_shortcut_analysis.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
