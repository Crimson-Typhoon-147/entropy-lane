import hashlib
import subprocess
import os
import random
import time

# 🌍 Curated busiest global locations (different time zones)
STREAM_POOL = [
    # 🇺🇸 New York (Times Square)
    "https://www.youtube.com/watch?v=rnXIjl_Rzy4",

    # 🇯🇵 Tokyo (Shibuya Crossing)
    "https://www.youtube.com/watch?v=dfVK7ld38Ys",

    # 🇬🇧 London (Abbey Road / streets)
    "https://www.youtube.com/watch?v=M3EYAY2MftI",

    # 🇦🇪 Dubai (Downtown / Sheikh Zayed Road)
    "https://www.youtube.com/watch?v=5uZa3-RMFos",

    # 🇸🇬 Singapore traffic cam
    "https://www.youtube.com/watch?v=AUlcCjfKZVE"
]


# 🔍 Check if stream is alive
def is_stream_alive(url):
    try:
        subprocess.check_output(
            ["yt-dlp", "-g", url],
            stderr=subprocess.DEVNULL
        )
        return True
    except:
        return False


# 🎯 Select active streams (max 3)
def get_active_streams(pool, k=3):
    random.shuffle(pool)

    active = []

    for url in pool:
        if is_stream_alive(url):
            active.append(url)

        if len(active) == k:
            break

    return active


# 📸 Capture frame from stream
def capture_frame(stream_url, output_file):
    try:
        stream = subprocess.check_output(
            ["yt-dlp", "-g", stream_url],
            stderr=subprocess.DEVNULL
        ).decode().strip()

        subprocess.run([
            "ffmpeg",
            "-loglevel", "quiet",
            "-i", stream,
            "-frames:v", "1",
            "-y",
            output_file
        ])

        if os.path.exists(output_file):
            with open(output_file, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()

    except:
        return None


# 🔥 MAIN FUNCTION
def get_traffic_entropy():
    try:
        streams = get_active_streams(STREAM_POOL, 3)

        hashes = []

        for i, url in enumerate(streams):
            h = capture_frame(url, f"frame_{i}.jpg")
            if h:
                hashes.append(h)

        # ❌ If all failed → fallback
        if not hashes:
            return hashlib.sha256(str(time.time_ns()).encode()).hexdigest()

        # 🔗 XOR mixing
        combined = 0
        for h in hashes:
            combined ^= int(h, 16)

        return hashlib.sha256(str(combined).encode()).hexdigest()

    except:
        # 🚨 Final fallback (never fail)
        return hashlib.sha256(str(time.time_ns()).encode()).hexdigest()


if __name__ == "__main__":
    print(get_traffic_entropy())