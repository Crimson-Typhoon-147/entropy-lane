import cv2
import os


def load_video_frames(video_path=None, target_fps=5, assumed_fps=30):
    """
    Load frames from a video file or webcam at a reduced frame rate.

    Args:
        video_path (str): Optional path to video file
        target_fps (int): Desired frame extraction rate
        assumed_fps (int): Fallback FPS if actual FPS is unavailable

    Returns:
        list: Extracted frames (grayscale)
    """

    # Get absolute path of current file directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Build absolute path if not provided
    if video_path is None:
        video_path = os.path.join(BASE_DIR, "..", "data", "video", "North.mp4")

    # Normalize path
    video_path = os.path.abspath(video_path)

    print(f"[DEBUG] Trying to open video: {video_path}")

    # Try opening video file
    cap = cv2.VideoCapture(video_path)
    source = "file"

    # 🔥 Fallback to webcam if file fails
    if not cap.isOpened():
        print("⚠️ Video file not found or cannot be opened. Falling back to webcam...")
        cap = cv2.VideoCapture(0)
        source = "webcam"

    # Final check
    if not cap.isOpened():
        raise ValueError("❌ No valid video source available (file/webcam both failed)")

    print(f"[DEBUG] Using source: {source}")

    # Get actual FPS
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    if actual_fps == 0 or actual_fps is None:
        actual_fps = assumed_fps

    frame_interval = max(1, int(actual_fps // target_fps))

    frames = []
    count = 0
    MAX_FRAMES = 100  # prevent excessive memory usage

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if count % frame_interval == 0:
            # Convert to grayscale (better for entropy consistency)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frames.append(frame)

        if len(frames) >= MAX_FRAMES:
            break

        count += 1

    cap.release()

    if len(frames) == 0:
        raise ValueError("❌ No frames extracted — video may be corrupted or capture failed")

    print(f"[DEBUG] Extracted {len(frames)} frames")

    return frames


# 🔹 Standalone testing
if __name__ == "__main__":
    frames = load_video_frames(target_fps=5)
    print("Frames extracted:", len(frames))