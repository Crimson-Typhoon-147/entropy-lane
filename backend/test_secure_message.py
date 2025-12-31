from entropy.video_loader import load_video_frames
from entropy.frame_preprocess import preprocess_frames
from entropy.feature_extract import extract_motion_features
from entropy.window_entropy import compute_entropy_windows
from entropy.entropy_pool import condition_entropy

from crypto.key_derivation import derive_key
from crypto.aes_gcm import encrypt_message, decrypt_message

# Step 1: Generate entropy
frames = load_video_frames("../data/video/North.mp4", target_fps=5)
frames = preprocess_frames(frames)
features = extract_motion_features(frames)

entropy_windows = compute_entropy_windows(features)
entropy_blocks = condition_entropy(entropy_windows)

# Step 2: Derive key
key = derive_key(entropy_blocks)

# Step 3: Encrypt message
message = "EntropyLane secure message"
nonce, ciphertext = encrypt_message(key, message)

# Step 4: Decrypt message
decrypted = decrypt_message(key, nonce, ciphertext)

print("Original message:", message)
print("Ciphertext (hex):", ciphertext.hex())
print("Decrypted message:", decrypted)
