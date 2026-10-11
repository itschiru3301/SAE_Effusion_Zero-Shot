"""SEM (Sparse Embedding Modulation, Guimard et al., CVPR 2026) applied to a chest X-ray backbone.

SEM debiases only the TEXT side: each class prompt is encoded into the latent space of a Matryoshka sparse autoencoder
(SAE) trained on the backbone's text embeddings; latents that respond to the spurious attribute (estimated from bias
prompts) are pulled toward their median over a set of neutral captions, latents that carry the class concept are
kept, and the result is decoded back into a text embedding. Images are untouched and nothing is fine-tuned.
  SEM_b   class prompt + bias prompts
  SEM_bi  class prompt + class paraphrases + bias prompts (the full method)
The SEM implementation is the authors' code (github.com/mardgui/SEM, pinned in scripts/setup.sh), used unchanged; this
module only routes its text encoding through our backbone.
"""
import os
import sys

import torch
import torch.nn.functional as F

from . import paths


def _import_sem():
    if paths.SEM_REPO not in sys.path:
        sys.path.insert(0, paths.SEM_REPO)
    import debiasing_methods.method_utils as mu
    import debiasing_methods.sem as sem_module
    return mu, sem_module


def build(backbone, version, sem_prompts, sae_path):
    """Returns a SEM object whose debias_text() gives debiased class embeddings."""
    mu, sem_module = _import_sem()

    def encode(text_prompts, model, normalize):
        e = model.encode_texts(list(text_prompts))
        return F.normalize(e, dim=-1) if normalize else e

    mu.get_clip_text_embedding = encode
    sem_module.get_clip_text_embedding = encode
    sem_module.diverse_prompts = sem_prompts["diverse prompts"]
    return sem_module.SEM({"clip_model": backbone, "sem_version": version, "sae_weights_path": sae_path})


def debiased_class_embeddings(backbone, version, sem_prompts, sae_path):
    sem = build(backbone, version, sem_prompts, sae_path)
    with torch.no_grad():
        t = sem.debias_text(sem_prompts["class prompts"], extra_prompts=sem_prompts)
    return F.normalize(t.float(), dim=-1)


def default_sae_path(backbone):
    return os.path.join(paths.ARTIFACTS, "sae",
                        f"MSAE_{backbone.name}_{backbone.embed_dim}_16384_256x512_reverse.pth")
