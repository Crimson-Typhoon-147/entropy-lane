from backend.entropy.video_loader import load_video_frames
from backend.entropy.frame_preprocess import preprocess_frames
from backend.entropy.feature_extract import extract_motion_features
from backend.entropy.window_entropy import compute_entropy_windows

frames = load_video_frames(target_fps=5)
frames = preprocess_frames(frames)
features = extract_motion_features(frames)

entropy_windows = compute_entropy_windows(features)

print("Total entropy windows:", len(entropy_windows))
print("First window entropy:", entropy_windows[0])
print("Last window entropy:", entropy_windows[-1])
