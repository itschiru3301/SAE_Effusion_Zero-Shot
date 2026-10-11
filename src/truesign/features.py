"""Image embeddings for the benchmark, computed once per backbone and cached in artifacts/."""
import os

import numpy as np
import torch
from PIL import Image
from torch.utils.data import DataLoader, Dataset

from . import paths


class _Images(Dataset):
    def __init__(self, files, preprocess):
        self.files, self.preprocess = files, preprocess

    def __len__(self):
        return len(self.files)

    def __getitem__(self, i):
        return self.preprocess(Image.open(os.path.join(paths.DATA_DIR, self.files[i])))


def image_features(backbone, files, recompute=False, batch_size=128, workers=8):
    """Raw image embeddings (N, d) in the order of `files`."""
    cache = os.path.join(paths.ARTIFACTS, "features", f"{backbone.name}.npz")
    if os.path.exists(cache) and not recompute:
        z = np.load(cache, allow_pickle=False)
        if list(z["files"]) == list(files):
            return torch.from_numpy(z["X"])
    feats = [backbone.encode_images(x).cpu()
             for x in DataLoader(_Images(files, backbone.preprocess), batch_size=batch_size, num_workers=workers)]
    X = torch.cat(feats)
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    np.savez(cache, X=X.numpy(), files=np.array(files))
    return X
