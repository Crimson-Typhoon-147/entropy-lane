import cv2

def load_video_frames(video_path, target_fps=5, assumed_fps=30):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Cannot open video file")

    frame_interval = int(assumed_fps // target_fps)
    frames = []
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if count % frame_interval == 0:
            frames.append(frame)

        count += 1

    cap.release()
    return frames


if __name__ == "__main__":
    frames = load_video_frames("../data/video/North.mp4", target_fps=5)
    print("Frames extracted:", len(frames))
