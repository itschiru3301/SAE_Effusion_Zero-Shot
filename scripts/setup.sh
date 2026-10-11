#!/usr/bin/env bash
# Fetch third-party code and model weights (not redistributed in this repository).
#   bash scripts/setup.sh
set -euo pipefail
cd "$(dirname "$0")/.."

# SEM (Guimard et al., CVPR 2026), MIT licence, pinned to the commit used for the reported results
mkdir -p third_party
if [ ! -d third_party/SEM ]; then
  git clone https://github.com/mardgui/SEM.git third_party/SEM
  git -C third_party/SEM checkout 554ffc550897e7a71e7ba7ce3fb727231014dc0f
fi

# CheXzero checkpoint (Tiu et al., 2022), from the authors' public folder (github.com/rajpurkarlab/CheXzero)
mkdir -p models/chexzero
if [ ! -f models/chexzero/best_64_5e-05_original_22000_0.864.pt ]; then
  python -m gdown --folder "https://drive.google.com/drive/folders/1makFLiEMbSleYltaRxw81aBhEDMpVwno" -O models/chexzero
  test -f models/chexzero/best_64_5e-05_original_22000_0.864.pt || {
    echo "Checkpoint not downloaded (Google Drive rate limit?). Download it manually into models/chexzero/."; exit 1; }
fi
echo "setup complete"
