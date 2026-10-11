"""Locations of data, model weights, third-party code and generated artifacts.

Every path can be overridden with an environment variable; defaults are relative to the repository root.
"""
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _env(name, default):
    return os.path.abspath(os.environ.get(name, default))


PADCHEST_DIR = _env("PADCHEST_DIR", os.path.join(ROOT, "data", "padchest_raw"))      # original PadChest PNGs + CSV
DATA_DIR = _env("TRUESIGN_DATA_DIR", os.path.join(ROOT, "data", "padchest_effusion"))   # built benchmark images
MODEL_DIR = _env("TRUESIGN_MODEL_DIR", os.path.join(ROOT, "models"))                    # downloaded weights
THIRD_PARTY = _env("TRUESIGN_THIRD_PARTY", os.path.join(ROOT, "third_party"))           # pinned SEM repository
ARTIFACTS = _env("TRUESIGN_ARTIFACTS", os.path.join(ROOT, "artifacts"))                 # features, trained SAEs
RESULTS = os.path.join(ROOT, "results")
PROMPTS = os.path.join(ROOT, "prompts")
SPLIT_FILE = os.path.join(ROOT, "benchmark", "padchest_effusion_split.csv")

PADCHEST_CSV = "PADCHEST_chest_x_ray_images_labels_160K_01.02.19.csv"
CHEXZERO_CKPT = os.path.join(MODEL_DIR, "chexzero", "best_64_5e-05_original_22000_0.864.pt")

SEM_REPO = os.path.join(THIRD_PARTY, "SEM")
