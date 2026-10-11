"""Step 2 (prerequisite for SEM): train a Matryoshka SAE on CheXzero text embeddings of general web captions.

  python experiments/02_train_text_sae.py --device cuda:0        # ~30 min on one GPU, downloads CC3M captions once
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from truesign import paths  # noqa: E402
from truesign.backbones import load_backbone  # noqa: E402
from truesign.sae import train  # noqa: E402
from truesign.sem_debias import default_sae_path  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--epochs", type=int, default=10)
    args = ap.parse_args()
    bb = load_backbone("chexzero", args.device)
    report = train(bb, default_sae_path(bb), epochs=args.epochs)
    json.dump(report, open(os.path.join(paths.RESULTS, "02_text_sae.json"), "w"), indent=2)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
