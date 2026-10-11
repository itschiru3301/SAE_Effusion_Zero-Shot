# Step 1: zero-shot CheXzero shortcut analysis

| | val | test |
|---|---|---|
| Effusion AUC | 0.886 | 0.866 |
| Overall accuracy | 0.815 | 0.795 |
| Worst-group accuracy | 0.540 | 0.510 |
| Accuracy, both cues agree with label | 0.960 | 0.960 |
| Accuracy, both cues contradict label | 0.620 | 0.620 |
| Shortcut AUC, view (AP vs PA) | 0.679 [0.63, 0.73] | 0.670 [0.63, 0.71] |
| Shortcut AUC, support device | 0.665 [0.61, 0.72] | 0.632 [0.59, 0.67] |

Per-group accuracy (test)

| Group | Accuracy |
|---|---|
| no_effusion, PA+no_device | 0.94 |
| no_effusion, PA+device | 0.87 |
| no_effusion, AP+no_device | 0.57 |
| no_effusion, AP+device | 0.51 |
| effusion, PA+no_device | 0.73 |
| effusion, PA+device | 0.82 |
| effusion, AP+no_device | 0.94 |
| effusion, AP+device | 0.98 |
