import numpy as np
from scipy.stats import entropy as scipy_entropy

def shannon_entropy(values):
    values = np.array(values)

    hist, _ = np.histogram(values, bins=256, density=False)
    prob = hist / np.sum(hist)

    prob = prob[prob > 0]

    return scipy_entropy(prob, base=2)

def min_entropy(values):
    values = np.array(values)

    probs = np.bincount(values.astype(int)) / len(values)

    return -np.log2(probs.max())

def compute_entropy_windows(features, window_size=15, step=7):
    entropy_results = []

    for i in range(0, len(features) - window_size + 1, step):
        window = features[i:i + window_size]

        entropy_results.append({
            "window_index": i,
            "shannon_entropy": shannon_entropy(window),
            "min_entropy": min_entropy(window)
        })

    return entropy_results