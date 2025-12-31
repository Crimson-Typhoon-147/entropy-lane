import numpy as np

def extract_motion_features(frames):
    """
    Extract motion-based features using frame-to-frame pixel differences.
    """
    features = []

    for i in range(1, len(frames)):
        diff = np.abs(frames[i].astype(np.int32) - frames[i-1].astype(np.int32))
        motion_intensity = np.sum(diff)
        features.append(motion_intensity)

    return features
