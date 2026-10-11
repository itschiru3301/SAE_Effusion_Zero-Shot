# All training-free methods evaluated (test split)

Same frozen CheXzero backbone, same blind prompts, same test split. Implementations: authors' code (SEM repository
re-implementations for RoboShot, PRISM, PRISM-mini; official code for Ortho-Proj / Ortho-Cali and FairerCLIP; TIE*
from the official notebook). Only SEM is included in this repository's code. Mean over 3 seeds where stochastic.

| Method | Worst-group acc. | Overall acc. |
|---|---|---|
| Zero-shot | 51.00 | 79.50 |
| SEM_b | 65.00 | 80.38 |
| SEM_bi | 60.00 | 80.75 |
| PRISM (ICCV 2025) | 49.33 ± 1.7 | 79.33 ± 0.1 |
| FairerCLIP, w/o labels (ICLR 2024) | 44.67 ± 0.9 | 77.96 ± 0.5 |
| RoboShot (ICLR 2024) | 40.00 | 76.75 |
| Ortho-Cali (Chuang et al. 2023) | 38.00 | 77.25 |
| Ortho-Proj (Chuang et al. 2023) | 28.00 | 74.62 |
| PRISM-mini (ICCV 2025) | 24.00 | 71.12 |
| TIE* (ICLR 2025) | 20.00 | 72.25 |

TIE (with ground-truth spurious labels) is not applicable under the blind-prompt protocol: the attribute it
would need labels for is the one proposed by the LLM, and mapping it onto the hidden groups would not be blind.
