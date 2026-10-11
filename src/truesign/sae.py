"""Matryoshka sparse autoencoder on a backbone's text embeddings (required by SEM).

The SAEs released with SEM are for OpenAI CLIP; CheXzero's text encoder is fine-tuned on radiology reports, so a new
SAE is trained with SEM's recipe: TopK Matryoshka SAE, latent 16384, TopK levels {256, 512}, reverse level weighting,
AdamW lr 1e-4, batch 2048, linear decay, on raw text embeddings of general web captions (Conceptual Captions 3M; SEM
used CC12M). The captions carry no information about the benchmark. Architecture = SEM's MatryoshkaSAE class.
"""
import json
import os

import numpy as np
import torch
import torch.nn.functional as F

from . import paths
from .sem_debias import _import_sem


def load_captions(cache=None):
    cache = cache or os.path.join(paths.ARTIFACTS, "sae", "cc3m_captions.json")
    if os.path.exists(cache):
        return json.load(open(cache))
    import pandas as pd
    from huggingface_hub import HfApi, hf_hub_download
    repo = "google-research-datasets/conceptual_captions"
    files = sorted(f for f in HfApi().list_repo_files(repo, repo_type="dataset") if f.endswith(".parquet") and "train" in f)
    caps = []
    for f in files:
        df = pd.read_parquet(hf_hub_download(repo, f, repo_type="dataset"))
        caps += df["caption"].astype(str).tolist()
    caps = list(dict.fromkeys(c.strip() for c in caps if c.strip()))
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    json.dump(caps, open(cache, "w"))
    return caps


def train(backbone, out_path, epochs=10, batch_size=2048, lr=1e-4, latent=16384, topk=(256, 512), seed=0):
    torch.manual_seed(seed)
    _, sem_module = _import_sem()
    dev = backbone.device
    emb_file = os.path.join(paths.ARTIFACTS, "sae", f"cc3m_{backbone.name}_text_emb.npy")
    if os.path.exists(emb_file):
        X = np.load(emb_file)
    else:
        caps = load_captions()
        X = np.concatenate([backbone.encode_texts(caps[s:s + 4096], truncate=True).cpu().numpy()
                            for s in range(0, len(caps), 4096)]).astype(np.float32)
        np.save(emb_file, X)
    X = torch.from_numpy(X)
    perm = torch.randperm(len(X))
    held, X = X[perm[:20000]], X[perm[20000:]]
    sae = sem_module.MatryoshkaSAE(X.shape[1], latent, list(topk), "reverse").to(dev)
    with torch.no_grad():
        sae.bpre.copy_(X.mean(0).to(dev))
    opt = torch.optim.AdamW(sae.parameters(), lr=lr)
    steps = epochs * (len(X) // batch_size)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda t: 1 - t / steps)
    for _ in range(epochs):
        order = torch.randperm(len(X))
        for s in range(0, len(X) - batch_size + 1, batch_size):
            loss = sae(X[order[s:s + batch_size]].to(dev))
            opt.zero_grad()
            loss.backward()
            opt.step()
            sched.step()
            with torch.no_grad():  # unit-norm decoder columns
                sae.decoder.weight.data = F.normalize(sae.decoder.weight.data, dim=0)
    with torch.no_grad():
        h = held.to(dev)
        cos = F.cosine_similarity(sae.reconstruct(h), h).mean().item()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    torch.save(sae.state_dict(), out_path)
    return {"weights": os.path.basename(out_path), "train_captions": len(X), "heldout_reconstruction_cosine": cos,
            "epochs": epochs, "batch_size": batch_size, "lr": lr, "latent": latent, "topk": list(topk)}
