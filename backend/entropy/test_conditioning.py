from entropy.video_loader import load_video_frames
from entropy.frame_preprocess import preprocess_frames
from entropy.feature_extract import extract_motion_features
from entropy.window_entropy import compute_entropy_windows
from entropy.entropy_pool import condition_entropy

frames = load_video_frames("../data/video/North.mp4", target_fps=5)
frames = preprocess_frames(frames)
features = extract_motion_features(frames)

entropy_windows = compute_entropy_windows(features)
entropy_blocks = condition_entropy(entropy_windows)

print("Total entropy blocks:", len(entropy_blocks))
print("First entropy block:", entropy_blocks[0])
print("Last entropy block:", entropy_blocks[-1])
