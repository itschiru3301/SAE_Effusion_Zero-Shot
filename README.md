# TrueSign-CXR: training-free mitigation of shortcut learning in a chest X-ray vision-language model

Zero-shot medical vision-language models can classify chest X-rays from a text prompt alone, but they inherit
correlations from their training data that are not the disease itself. This project shows that CheXzero, a CLIP model
trained on MIMIC-CXR radiology reports, partly detects pleural effusion from *how and where* an image was taken
(portable bedside films, visible tubes and lines) rather than from the effusion, and that this can be reduced
**without any retraining or labelled data** by editing only the class text embeddings.

On a balanced benchmark built from PadChest, SEM text-embedding modulation raises worst-group accuracy from
**51.0 % to 65.0 %** while overall accuracy rises slightly (79.5 % to 80.4 %), using frozen image features and no labels.

## Problem and benchmark

In hospital data, effusion is common in sicker, often bedridden patients. Their X-rays are typically portable
anteroposterior (AP) films and frequently show support devices. A model can therefore score "effusion" from the
acquisition context. To measure this, I built **PadChest-Effusion**, an UrbanCars-style benchmark with two spurious
attributes:

| | Value 0 | Value 1 |
|---|---|---|
| Target | no pleural effusion | pleural effusion |
| Spurious attribute 1: view | PA (standing) | AP / AP-horizontal (bedside) |
| Spurious attribute 2: support device | none | tube, central line, catheter, pacemaker |

- Source: PadChest frontal radiographs (107,108 after label filtering). Images with a chest drain were excluded because a
  drain is a treatment for effusion and would leak the label.
- 8 groups (effusion x view x device). Patient-disjoint splits. Test: 100 images per group; validation: 50 per group;
  training: 1,143 per class with view and device each 95 % aligned with the label (used only by methods that need
  unlabelled images; SEM does not).
- In the raw data the correlation is real: 53 % of effusion images are AP versus 15 % of the rest, and 38 % show a
  device versus 9 %.

## Step 1: the zero-shot model relies on the shortcuts

Backbone selection was done on the validation split (`results/backbone_selection.md`): of six chest X-ray
vision-language models, CheXzero was the only one that was both accurate (AUC 0.886) and sensitive to both cues.

Zero-shot CheXzero on the test split (`results/01_shortcut_analysis.md`):

| Metric | Test |
|---|---|
| Effusion AUC | 0.866 |
| Overall accuracy | 0.795 |
| Worst-group accuracy | 0.510 |
| Accuracy when both cues agree with the label | 0.960 |
| Accuracy when both cues contradict the label | 0.620 |
| Shortcut AUC, view (AP vs PA) | 0.670 [0.63, 0.71] |
| Shortcut AUC, support device | 0.632 [0.59, 0.67] |

The shortcut AUC measures, within each true class, how well the effusion score alone separates AP from PA (or device
from no device); 0.5 would mean the cue has no effect. Both are clearly above 0.5. The failure is concentrated where
the cues point the wrong way: patients **without** effusion imaged at the bedside with a device are classified
correctly only 51 % of the time, versus 94 % for standing films without devices.

## Step 2: mitigation without retraining

**Method.** SEM (Sparse Embedding Modulation, CVPR 2026) edits only the two class text embeddings.
Each class prompt is mapped into the latent space of a sparse autoencoder trained on the model's text embeddings.
Latent features that respond to the spurious attribute, estimated from short descriptions of it, are pulled toward
their value on neutral captions, features that carry the disease concept are kept, and the result is decoded back.
Images, the image encoder and the classifier are untouched.

**Blind prompts.** The descriptions of spurious attributes were written by a separate LLM instance that was told only
the task (effusion vs no effusion on chest X-rays) and the required format, with no access to how the benchmark groups
were built (`prompts/generation/`: brief, verbatim response, checksums). It proposed "portable supine AP vs upright PA"
and "support devices" from general radiology knowledge. Class prompts are the CheXzero authors' own zero-shot pair.

**Adapting SEM to a medical model.** SEM's released autoencoders are for OpenAI CLIP. I trained a Matryoshka sparse
autoencoder on CheXzero's text encoder with SEM's recipe on 2.3 M general web captions (held-out reconstruction cosine
0.998; `results/02_text_sae.json`). The caption corpus contains nothing about the benchmark.

## Step 3: results

Test split, same frozen image features for every row (`results/03_mitigation.md`):

| Metric | Zero-shot | SEM_b | SEM_bi |
|---|---|---|---|
| Worst-group accuracy | 0.510 | **0.650** | 0.600 |
| Overall accuracy | 0.795 | 0.804 | **0.807** |
| Accuracy, both cues contradict the label | 0.620 | **0.680** | 0.650 |
| Shortcut AUC, view | 0.670 | **0.595** | 0.624 |
| Shortcut AUC, device | 0.632 | 0.622 | 0.635 |

SEM_b uses the class prompt and the spurious-attribute descriptions; SEM_bi additionally uses class paraphrases.

| Group (test) | Zero-shot | SEM_b | SEM_bi |
|---|---|---|---|
| no effusion, PA, no device | 0.94 | 0.97 | 0.97 |
| no effusion, PA, device | 0.87 | 0.89 | 0.89 |
| no effusion, AP, no device | 0.57 | 0.69 | 0.67 |
| no effusion, AP, device | 0.51 | 0.65 | 0.60 |
| effusion, PA, no device | 0.73 | 0.71 | 0.70 |
| effusion, PA, device | 0.82 | 0.79 | 0.82 |
| effusion, AP, no device | 0.94 | 0.84 | 0.87 |
| effusion, AP, device | 0.98 | 0.89 | 0.94 |

**Findings**
- Editing two text embeddings, with no labels and no gradient updates to the model, removes a large part of the
  bedside-film shortcut: the worst group improves by 14 points and the view shortcut AUC falls from 0.670 to 0.595.
- The gain is a trade-off, not free accuracy: false "effusion" calls on bedside films drop, while some true effusions on
  bedside films are missed (0.98 to 0.89). Overall accuracy is unchanged to slightly better.
- The device shortcut is barely reduced (0.632 to 0.622), so device-related bias remains an open problem.
- Seven other training-free methods were evaluated in the same setting (`results/all_methods.md`). Only the SEM variants
  improved the worst group; projection-based methods made it worse, because in this model's text space the
  "portable / supine / tubes" directions overlap with the effusion direction itself.

**Limitations.** One dataset and one finding; 100 test images per group (differences of a few points are within noise;
confidence intervals are given for the shortcut statistics); labels are partly report-derived; the view effect is
partly genuine anatomy (AP films magnify the heart and lower lung volumes), so the device effect is the cleaner
evidence of a learned spurious correlation.

## Reproducing

Requirements: Python 3.10, one GPU, a local copy of PadChest (research-use agreement from BIMCV), and the packages in
`requirements.txt`.

```
pip install -r requirements.txt
bash scripts/setup.sh                                          # SEM (pinned commit) + CheXzero checkpoint
PADCHEST_DIR=/path/to/padchest python experiments/00_build_benchmark.py
python experiments/01_shortcut_analysis.py --device cuda:0
python experiments/02_train_text_sae.py   --device cuda:0      # about 30 min; downloads Conceptual Captions once
python experiments/03_mitigation.py       --device cuda:0
```

PadChest images and labels are not redistributed: `benchmark/padchest_effusion_split.csv` contains only image IDs and
their split, and `00_build_benchmark.py` recomputes all labels from the official PadChest CSV.

## Repository layout

```
benchmark/padchest_effusion_split.csv   PadChest image IDs and split (0 train, 1 val, 2 test)
prompts/zero_shot.json                  class prompts (CheXzero authors' zero-shot pair)
prompts/sem.json                        SEM inputs: blind spurious-attribute descriptions, class paraphrases
prompts/generation/                     blind prompt-generation brief, verbatim LLM response, checksums
src/truesign/                              backbone, data, prompts, features, metrics, SAE training, SEM wrapper
experiments/00-03                       benchmark build, shortcut analysis, SAE training, mitigation
results/                                outputs of the experiments plus backbone selection and all-method comparison
scripts/setup.sh                        third-party code and weights
```

## References

- Tiu et al., Expert-level detection of pathologies from unannotated chest X-ray images via self-supervised learning
  (CheXzero), Nature Biomedical Engineering, 2022. github.com/rajpurkarlab/CheXzero
- Guimard et al., SEM: Sparse Embedding Modulation for Post-Hoc Debiasing of Vision-Language Models, CVPR 2026,
  arXiv:2603.19028. github.com/mardgui/SEM (code used unchanged)
- Bustos et al., PadChest: a large chest X-ray image dataset with multi-label annotated reports, Medical Image
  Analysis, 2020.
- Li et al., A Whac-A-Mole Dilemma: shortcuts come in multiples where mitigating one amplifies others (UrbanCars),
  CVPR 2023.
- Sharma et al., Conceptual Captions, ACL 2018.
