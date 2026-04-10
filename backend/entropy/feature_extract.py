import numpy as np
import cv2

def extract_motion_features(frames):
    """
    Extract multiple motion-based entropy features.
    Returns a richer feature vector.
    """

    features = []

    for i in range(1, len(frames)):
        prev = frames[i - 1].astype(np.int32)
        curr = frames[i].astype(np.int32)

        diff = np.abs(curr - prev)

        # 1️⃣ Mean motion
        mean_motion = np.mean(diff)

        # 2️⃣ Variance (important for entropy)
        variance_motion = np.var(diff)

        # 3️⃣ Edge-based randomness
        edges = cv2.Canny(curr.astype(np.uint8), 100, 200)
        edge_density = np.sum(edges) / edges.size

        # 4️⃣ Pixel intensity randomness
        intensity_std = np.std(curr)

        # Combine features (VERY IMPORTANT)
        combined_feature = (
            mean_motion +
            variance_motion +
            edge_density * 1000 +
            intensity_std
        )

        features.append(combined_feature)

    return features