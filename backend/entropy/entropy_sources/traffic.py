import hashlib
import subprocess
import os
import random
import time
import numpy as np
import cv2

# Import your existing validation logic
# Note: Adjust these imports if your folder structure differs
from entropy.window_entropy import shannon_entropy
from entropy.feature_extract import extract_motion_features

# 🌍 Curated busiest global locations
STREAM_POOL = [
    "https://www.youtube.com/watch?v=rnXIjl_Rzy4", # NYC
    "https://www.youtube.com/watch?v=dfVK7ld38Ys", # Tokyo
    "https://www.youtube.com/watch?v=M3EYAY2MftI", # London
    "https://www.youtube.com/watch?v=5uZa3-RMFos", # Dubai
    "https://www.youtube.com/watch?v=AUlcCjfKZVE"  # Singapore
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
    """
    Captures a small burst of frames to measure MOTION and ENTROPY.
    """
    frames = []
    try:
        stream = subprocess.check_output(["yt-dlp", "-g", stream_url], stderr=subprocess.DEVNULL).decode().strip()
        
        for i in range(num_frames):
            temp_file = f"temp_frame_{i}.jpg"
            subprocess.run([
                "ffmpeg", "-loglevel", "quiet", "-i", stream,
                "-frames:v", "1", "-y", temp_file
            ])
            
            if os.path.exists(temp_file):
                img = cv2.imread(temp_file, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    frames.append(img)
                os.remove(temp_file)
            time.sleep(0.5) # Short gap to capture motion
            
        return frames
    except Exception as e:
        print(f"Capture Error: {e}")
        return []

def get_traffic_entropy():
    """
    BUSINESS GRADE: Validates visual chaos before returning a hash.
    """
    try:
        streams = get_active_streams(STREAM_POOL, 1)
        if not streams:
            return fallback_entropy()

        frames = capture_entropy_frames(streams[0])
        if len(frames) < 2:
            return fallback_entropy()

        # 1. Measure Visual Randomness (Shannon Entropy)
        # Using your window_entropy.py logic
        h_score = shannon_entropy(frames[0].flatten())
        
        # 2. Measure Motion Randomness (Variance)
        # Using your feature_extract.py logic
        motion_features = extract_motion_features(frames)
        motion_score = np.var(motion_features) if motion_features else 0

        # 🔥 THRESHOLD CHECK (The "Business Rule")
        # If the camera is static (night/frozen), h_score or motion_score will be low
        if h_score < 7.0 or motion_score < 0.01:
            print(f"⚠️ Low Entropy Source Detected (H:{h_score:.2f}, M:{motion_score:.2f}). Rejecting.")
            return fallback_entropy()

        # 3. Create Final Seed from Validated Chaos
        combined_data = "".join([hashlib.sha256(f.tobytes()).hexdigest() for f in frames])
        return hashlib.sha256(combined_data.encode()).hexdigest()

    except Exception as e:
        print(f"Traffic Oracle Error: {e}")
        return fallback_entropy()

def fallback_entropy():
    # Use nanosecond precision and system noise as a safety net
    raw = f"{time.time_ns()}{os.getpid()}{random.random()}"
    return hashlib.sha256(raw.encode()).hexdigest()

if __name__ == "__main__":
    print("Traffic Oracle Output:", get_traffic_entropy())