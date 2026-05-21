import hashlib
import subprocess
import os
import random
import time
import numpy as np
import cv2

from entropy.window_entropy import shannon_entropy
from entropy.feature_extract import extract_motion_features

STREAM_POOL = [
    "https://www.youtube.com/watch?v=rnXIjl_Rzy4",
    "https://www.youtube.com/watch?v=dfVK7ld38Ys",
    "https://www.youtube.com/watch?v=M3EYAY2MftI",
    "https://www.youtube.com/watch?v=5uZa3-RMFos",
    "https://www.youtube.com/watch?v=AUlcCjfKZVE"
]

def is_stream_alive(url):
    try:
        subprocess.check_output(["yt-dlp", "-g", url], stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def get_active_streams(pool, k=2):
    random.shuffle(pool)
    active = []
    for url in pool:
        if is_stream_alive(url):
            active.append(url)
        if len(active) == k:
            break
    return active


def capture_entropy_frames(stream_url, num_frames=5):
    frames = []
    try:
        stream = subprocess.check_output(
            ["yt-dlp", "-g", stream_url],
            stderr=subprocess.DEVNULL
        ).decode().strip()

        for i in range(num_frames):
            temp_file = f"temp_frame_{i}.jpg"

            subprocess.run([
                "ffmpeg", "-loglevel", "quiet",
                "-i", stream,
                "-frames:v", "1",
                "-y", temp_file
            ])

            if os.path.exists(temp_file):
                img = cv2.imread(temp_file, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    frames.append(img)
                os.remove(temp_file)

            time.sleep(0.3)

        return frames

    except Exception as e:
        print(f"❌ Capture Error: {e}")
        return []


def get_traffic_entropy():
    """
    🔥 STRICT VALIDATION MODE
    Returns None if entropy is weak (NO FALLBACK HERE)
    """
    try:
        streams = get_active_streams(STREAM_POOL, 1)
        if not streams:
            print("❌ No active streams")
            return None

        frames = capture_entropy_frames(streams[0])

        if len(frames) < 2:
            print("❌ Not enough frames")
            return None

        # 📊 Shannon Entropy
        h_score = shannon_entropy(frames[0].flatten())

        # 📊 Motion randomness
        motion_features = extract_motion_features(frames)
        motion_score = np.var(motion_features) if motion_features else 0

        print(f"📊 Traffic Entropy → H:{h_score:.2f} | Motion:{motion_score:.4f}")

        # 🔥 RELAXED THRESHOLDS (real-world tuned)
        if h_score < 6.5 or motion_score < 0.005:
            print("⚠️ Weak traffic entropy → DROPPED")
            return None   # ❌ IMPORTANT CHANGE

        # 🔐 Final seed
        combined_data = "".join([
            hashlib.sha256(f.tobytes()).hexdigest()
            for f in frames
        ])

        return hashlib.sha256(combined_data.encode()).hexdigest()

    except Exception as e:
        print(f"❌ Traffic Oracle Error: {e}")
        return None