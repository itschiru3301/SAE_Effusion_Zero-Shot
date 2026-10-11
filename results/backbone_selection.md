# Backbone selection (validation split only)

Each model used its own published zero-shot recipe. Shortcut AUC: within each true class, AUC of the effusion
score for AP vs PA (view) and device vs none (device); 0.5 = no shortcut. 95 % bootstrap intervals.

| Model | Effusion AUC | Shortcut AUC, view | Shortcut AUC, device | Worst-group acc. | Overall acc. |
|---|---|---|---|---|---|
| CheXzero | 0.886 | 0.679 [0.63, 0.73] | 0.665 [0.61, 0.72] | 0.54 | 0.81 |
| BioViL-T | 0.808 | 0.843 [0.81, 0.88] | 0.561 [0.50, 0.62] | 0.28 | 0.76 |
| BioViL | 0.870 | 0.786 [0.74, 0.83] | 0.549 [0.49, 0.61] | 0.42 | 0.79 |
| MedCLIP-ResNet | 0.852 | 0.769 [0.73, 0.82] | 0.575 [0.52, 0.63] | 0.58 | 0.82 |
| MedCLIP-ViT | 0.925 | 0.517 [0.46, 0.58] | 0.570 [0.51, 0.63] | 0.32 | 0.74 |
| BiomedCLIP | 0.828 | 0.677 [0.62, 0.73] | 0.590 [0.53, 0.64] | 0.12 | 0.59 |

CheXzero is the only model that is both accurate and follows both cues; it was selected before any
debiasing method was evaluated, and the test split was not used for the selection.
