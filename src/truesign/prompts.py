"""Prompt files: prompts/zero_shot.json and prompts/sem.json.

zero_shot.json  "class prompts": {"no_effusion": str, "effusion": str}
sem.json        "class prompts", "bias prompts": {spurious value: [str]}, "extra class prompts": {class: [str]},
                "diverse prompts": [str]
The spurious values in sem.json were proposed by a blind LLM (prompts/generation/) and are not the benchmark's groups.
"""
import json
import os

from . import paths
from .data import CLASS_NAMES

REQUIRED = {"zero_shot": ["class prompts"],
            "sem": ["class prompts", "bias prompts", "extra class prompts", "diverse prompts"]}


def _by_class(value, what, path):
    missing = [c for c in CLASS_NAMES if c not in value]
    if missing:
        raise ValueError(f"{path}: '{what}' is missing {missing}")
    return [value[c] for c in CLASS_NAMES]


def load(name, prompt_dir=paths.PROMPTS):
    path = os.path.join(prompt_dir, f"{name}.json")
    raw = json.load(open(path))
    for k in REQUIRED[name]:
        if k not in raw:
            raise ValueError(f"{path}: missing '{k}'")
    p = dict(raw)
    p["class prompts"] = _by_class(raw["class prompts"], "class prompts", path)
    if name == "sem":
        p["extra class prompts"] = _by_class(raw["extra class prompts"], "extra class prompts", path)
    return p
