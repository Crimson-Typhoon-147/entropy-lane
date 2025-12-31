from entropy.video_loader import load_video_frames
from entropy.frame_preprocess import preprocess_frames

frames = load_video_frames("../data/video/North.mp4", target_fps=5)
processed = preprocess_frames(frames)

print("Raw frames:", len(frames))
print("Processed frames:", len(processed))
print("Frame shape:", processed[0].shape)
