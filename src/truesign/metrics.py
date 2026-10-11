"""Group accuracies, worst-group accuracy and shortcut statistics."""
import numpy as np
from sklearn.metrics import roc_auc_score

from .data import CLASS_NAMES, GROUP_NAMES


def group_metrics(pred, y, group):
    correct = pred == y
    groups = {}
    for yy in (0, 1):
        for g in range(len(GROUP_NAMES)):
            m = (y == yy) & (group == g)
            if m.any():
                groups[f"{CLASS_NAMES[yy]}|{GROUP_NAMES[g]}"] = {"acc": float(correct[m].mean()), "n": int(m.sum())}
    return {"worst": min(v["acc"] for v in groups.values()), "overall": float(correct.mean()), "groups": groups}


def summarize_runs(runs):
    """Mean / std over seeds; per-group values from the first run are kept in 'runs'."""
    return {"worst": float(np.mean([r["worst"] for r in runs])), "overall": float(np.mean([r["overall"] for r in runs])),
            "worst_std": float(np.std([r["worst"] for r in runs])),
            "overall_std": float(np.std([r["overall"] for r in runs])), "runs": runs}


def within_class_auc(score, y, attribute):
    """Mean over the two classes of AUC(score separates attribute=1 from attribute=0). 0.5 = no shortcut."""
    return float(np.mean([roc_auc_score(attribute[y == c], score[y == c]) for c in (0, 1)]))


def bootstrap_ci(fn, n, B=1000, seed=0):
    rng = np.random.RandomState(seed)
    vals = [fn(rng.randint(0, n, n)) for _ in range(B)]
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]
