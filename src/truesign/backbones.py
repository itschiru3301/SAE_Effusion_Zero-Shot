"""Vision-language backbone interface.

    bb = load_backbone("chexzero", device)
    bb.preprocess(pil_image) -> tensor          model-specific preprocessing
    bb.encode_images(batch)  -> (N, d) float    raw (un-normalised) image embeddings
    bb.encode_texts(list)    -> (N, d) float    raw text embeddings, cached per prompt list

chexzero: CheXzero (Tiu et al., Nature Biomedical Engineering 2022), OpenAI CLIP ViT-B/32 fine-tuned on MIMIC-CXR
          image-report pairs; checkpoint best_64_5e-05_original_22000_0.864.pt. Preprocessing follows CheXzero
          data_process.preprocess and zero_shot.py.
"""
import numpy as np
import torch
from PIL import Image

from . import paths


class Backbone:
    name = None
    embed_dim = 512

    def __init__(self, device):
        self.device = device
        self._text_cache = {}

    def encode_texts(self, texts, truncate=False):
        key = (tuple(texts), truncate)
        if key not in self._text_cache:
            with torch.no_grad():
                self._text_cache[key] = self._encode_texts(list(texts), truncate).float()
        return self._text_cache[key].clone()

    def encode_images(self, pixels):
        with torch.no_grad():
            return self._encode_images(pixels.to(self.device)).float()

    @property
    def text_projection(self):
        """Some third-party method code reads model.text_projection.device to place tensors."""
        return self._device_anchor


class CheXzero(Backbone):
    name = "CheXzero"

    def __init__(self, device, checkpoint=paths.CHEXZERO_CKPT):
        super().__init__(device)
        import clip
        from torchvision.transforms import Compose, InterpolationMode, Normalize, Resize
        self._clip = clip
        model, _ = clip.load("ViT-B/32", device="cpu", jit=False)
        model.load_state_dict(torch.load(checkpoint, map_location="cpu"))
        self.model = model.to(device).eval().float()
        self._device_anchor = self.model.text_projection
        self._tf = Compose([Normalize((101.48761,) * 3, (83.43944,) * 3),
                            Resize(224, interpolation=InterpolationMode.BICUBIC)])

    def preprocess(self, img):
        # keep aspect ratio, longest side 320, zero-pad to 320 x 320, raw 0-255 values, 3 channels
        img = img.convert("L")
        r = 320 / max(img.size)
        img = img.resize((max(1, round(img.size[0] * r)), max(1, round(img.size[1] * r))), Image.LANCZOS)
        sq = Image.new("L", (320, 320))
        sq.paste(img, ((320 - img.size[0]) // 2, (320 - img.size[1]) // 2))
        return self._tf(torch.from_numpy(np.asarray(sq, dtype=np.float32))[None].repeat(3, 1, 1))

    def _encode_texts(self, texts, truncate):
        return self.model.encode_text(self._clip.tokenize(texts, truncate=truncate).to(self.device))

    def _encode_images(self, x):
        return self.model.encode_image(x)


BACKBONES = {"chexzero": CheXzero}


def load_backbone(name, device):
    return BACKBONES[name](device)
