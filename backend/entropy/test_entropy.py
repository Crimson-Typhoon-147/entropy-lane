from entropy.video_loader import load_video_frames
from entropy.frame_preprocess import preprocess_frames
from entropy.feature_extract import extract_motion_features
from entropy.window_entropy import compute_entropy_windows

frames = load_video_frames("../data/video/North.mp4", target_fps=5)
frames = preprocess_frames(frames)
features = extract_motion_features(frames)

entropy_windows = compute_entropy_windows(features)

print("Total entropy windows:", len(entropy_windows))
print("First window entropy:", entropy_windows[0])
print("Last window entropy:", entropy_windows[-1])
