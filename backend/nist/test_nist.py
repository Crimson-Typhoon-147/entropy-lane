from entropy.video_loader import load_video_frames
from entropy.frame_preprocess import preprocess_frames
from entropy.feature_extract import extract_motion_features
from entropy.window_entropy import compute_entropy_windows
from entropy.entropy_pool import condition_entropy

from nist.bitstream import entropy_blocks_to_bitstream
from nist.frequency_test import frequency_test
from nist.runs_test import runs_test

frames = load_video_frames("../data/video/North.mp4", target_fps=5)
frames = preprocess_frames(frames)
features = extract_motion_features(frames)

entropy_windows = compute_entropy_windows(features)
entropy_blocks = condition_entropy(entropy_windows)

bitstream = entropy_blocks_to_bitstream(entropy_blocks)

freq_result = frequency_test(bitstream)
runs_result = runs_test(bitstream)

print("Frequency Test:", freq_result)
print("Runs Test:", runs_result)

