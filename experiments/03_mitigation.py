"""Step 3: mitigate the shortcut without retraining (SEM text-embedding modulation) and compare with zero-shot.

All methods use the same frozen CheXzero image embeddings; only the two class text embeddings change.
  zero-shot  class prompts as given
  SEM_b      class prompt + bias prompts (blind LLM)
  SEM_bi     class prompt + class paraphrases + bias prompts (full SEM)
Reported on val and test: overall / worst-group accuracy, per-group accuracy, and the shortcut AUCs of step 1
recomputed on the debiased scores.
  python experiments/03_mitigation.py --device cuda:0
"""
import argparse
import importlib
import json
import os
import sys

import torch.nn.functional as F

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from truesign import paths, prompts  # noqa: E402
from truesign.backbones import load_backbone  # noqa: E402
from truesign.data import SPLITS, load_metadata  # noqa: E402
from truesign.features import image_features  # noqa: E402
from truesign.sem_debias import debiased_class_embeddings, default_sae_path  # noqa: E402

analyse = importlib.import_module("01_shortcut_analysis").analyse
METHODS = [("zero-shot", None), ("SEM_b", "SEM_b"), ("SEM_bi", "SEM_bi")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--sae", default=None, help="default: artifacts/sae/MSAE_CheXzero_512_16384_256x512_reverse.pth")
    args = ap.parse_args()
    meta = load_metadata()
    bb = load_backbone("chexzero", args.device)
    sae = args.sae or default_sae_path(bb)
    X = F.normalize(image_features(bb, meta["files"]).to(args.device), dim=-1)
    sem_prompts = prompts.load("sem")
    out = {}
    for name, version in METHODS:
        if version is None:
            t = F.normalize(bb.encode_texts(prompts.load("zero_shot")["class prompts"]), dim=-1)
        else:
            t = debiased_class_embeddings(bb, version, sem_prompts, sae)
        score = (X @ t[1] - X @ t[0]).cpu().numpy()
        out[name] = {}
        for split in ("val", "test"):
            m = meta["split"] == SPLITS[split]
            out[name][split] = analyse(score[m], meta["y"][m], meta["view"][m], meta["device"][m], meta["group"][m])
    json.dump(out, open(os.path.join(paths.RESULTS, "03_mitigation.json"), "w"), indent=2)

    names = [n for n, _ in METHODS]
    lines = ["# Step 3: mitigation without retraining (test split)", "",
             "| Metric | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
    for k, lab in (("worst", "Worst-group accuracy"), ("overall", "Overall accuracy"),
                   ("acc_cues_contradict", "Accuracy, both cues contradict label"),
                   ("shortcut_auc_view", "Shortcut AUC, view"), ("shortcut_auc_device", "Shortcut AUC, device")):
        lines.append(f"| {lab} | " + " | ".join(f"{out[n]['test'][k]:.3f}" for n in names) + " |")
    lines += ["", "| Group (test) | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
    for g in out["zero-shot"]["test"]["groups"]:
        lines.append(f"| {g.replace('|', ', ')} | " + " | ".join(f"{out[n]['test']['groups'][g]['acc']:.2f}" for n in names) + " |")
    open(os.path.join(paths.RESULTS, "03_mitigation.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
