# Step 3: mitigation without retraining (test split)

| Metric | zero-shot | SEM_b | SEM_bi |
|---|---|---|---|
| Worst-group accuracy | 0.510 | 0.650 | 0.600 |
| Overall accuracy | 0.795 | 0.804 | 0.807 |
| Accuracy, both cues contradict label | 0.620 | 0.680 | 0.650 |
| Shortcut AUC, view | 0.670 | 0.595 | 0.624 |
| Shortcut AUC, device | 0.632 | 0.622 | 0.635 |

| Group (test) | zero-shot | SEM_b | SEM_bi |
|---|---|---|---|
| no_effusion, PA+no_device | 0.94 | 0.97 | 0.97 |
| no_effusion, PA+device | 0.87 | 0.89 | 0.89 |
| no_effusion, AP+no_device | 0.57 | 0.69 | 0.67 |
| no_effusion, AP+device | 0.51 | 0.65 | 0.60 |
| effusion, PA+no_device | 0.73 | 0.71 | 0.70 |
| effusion, PA+device | 0.82 | 0.79 | 0.82 |
| effusion, AP+no_device | 0.94 | 0.84 | 0.87 |
| effusion, AP+device | 0.98 | 0.89 | 0.94 |
