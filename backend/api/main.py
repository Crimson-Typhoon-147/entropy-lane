from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

# ---------- Entropy pipeline imports ----------
from entropy.video_loader import load_video_frames
from entropy.frame_preprocess import preprocess_frames
from entropy.feature_extract import extract_motion_features
from entropy.window_entropy import compute_entropy_windows
from entropy.entropy_pool import condition_entropy

# ---------- Crypto imports ----------
from crypto.aes_gcm import encrypt_message, decrypt_message
from crypto.key_derivation import derive_aes_key

# ======================================================
# FASTAPI APP
# ======================================================

app = FastAPI()

# ---------- CORS (REQUIRED FOR REACT) ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# SESSION-LEVEL ENTROPY SETUP
# ======================================================

VIDEO_PATH = "../data/video/North.mp4"

# 1. Load video frames (ONCE)
frames = load_video_frames(VIDEO_PATH, target_fps=5)

# 2. Preprocess frames
frames = preprocess_frames(frames)

# 3. Extract motion-based features
features = extract_motion_features(frames)

# 4. Compute entropy over sliding windows
entropy_windows = compute_entropy_windows(features)

# 5. Pool & condition entropy
entropy_blocks = condition_entropy(entropy_windows)

# ---- Entropy consumption state (CRITICAL) ----
entropy_index = 0
TOTAL_ENTROPY_BLOCKS = len(entropy_blocks)

# ======================================================
# REQUEST MODELS
# ======================================================

class MessageRequest(BaseModel):
    message: str

# ======================================================
# API ENDPOINT
# ======================================================

@app.post("/send_message")
def send_message(req: MessageRequest):
    global entropy_index

    # ---- Enforce one-time entropy usage ----
    if entropy_index >= TOTAL_ENTROPY_BLOCKS:
        raise HTTPException(
            status_code=503,
            detail="Entropy exhausted. Restart service to regenerate entropy."
        )

    # Consume entropy block exactly once
    raw_entropy = entropy_blocks[entropy_index]
    entropy_index += 1

    # Convert entropy to bytes
    entropy_bytes = np.array(raw_entropy).tobytes()

    # Derive AES-256 key
    session_key = derive_aes_key(entropy_bytes)

    plaintext = req.message

    # Encrypt using AES-GCM
    nonce, ciphertext = encrypt_message(session_key, plaintext)

    # Decrypt (receiver-side simulation)
    decrypted = decrypt_message(session_key, nonce, ciphertext)

    # ---- FRONTEND-FRIENDLY RESPONSE ----
    return {
    "reply": decrypted,
    "ciphertext": ciphertext.hex(),
    "nonce": nonce.hex(),
    "entropy_index": entropy_index - 1,
    "algorithm": "AES-256-GCM",
    "entropy_source": "Traffic video motion"
}
