import numpy as np
from scipy.stats import entropy as scipy_entropy

def shannon_entropy(values):
    values = np.array(values)
    hist, _ = np.histogram(values, bins=256, density=True)
    return scipy_entropy(hist, base=2)

def min_entropy(values):
    values = np.array(values)
    probs = np.bincount(values.astype(int)) / len(values)
    return -np.log2(probs.max())

def compute_entropy_windows(features, window_size=15, step=7):
    """
    Sliding window entropy computation.
    window_size = 3 seconds (15 frames at 5 FPS)
    step = overlap of ~50%
    """
    entropy_results = []

    for i in range(0, len(features) - window_size, step):
        window = features[i:i + window_size]

        entropy_results.append({
            "window_index": i,
            "shannon_entropy": shannon_entropy(window),
            "min_entropy": min_entropy(window)
        })

    return entropy_results
