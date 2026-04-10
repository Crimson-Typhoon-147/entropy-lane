from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib
import time

# 🔥 Entropy system
from entropy.entropy_mixer import mix_entropy

# 🔐 Commit-Reveal
from entropy.commit_reveal import create_commit, reveal_commit, verify_commit, mark_commit_used

# 🔐 Crypto
from crypto.aes_gcm import encrypt_message
from crypto.key_derivation import derive_aes_key

# ======================================================
# FASTAPI APP
# ======================================================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# CHAT STORAGE
# ======================================================

CHAT_ROOMS = {}

# ======================================================
# MODELS
# ======================================================

class MessageRequest(BaseModel):
    roomId: str
    senderId: str
    message: str
    commit_id: str | None = None

# ======================================================
# COMMIT ENDPOINT
# ======================================================

@app.post("/commit")
def commit_entropy():
    commit_id, commit_hash = create_commit()
    return {"commit_id": commit_id, "commit_hash": commit_hash}

# ======================================================
# REVEAL ENDPOINT
# ======================================================

@app.get("/reveal/{commit_id}")
def reveal_entropy(commit_id: str):
    data = reveal_commit(commit_id)

    if not data:
        raise HTTPException(400, "Invalid or expired commit ID")

    return data

# ======================================================
# VERIFY ENDPOINT
# ======================================================

@app.post("/verify")
def verify_entropy(entropy: str, secret: str, commit: str):
    valid = verify_commit(entropy, secret, commit)
    return {"valid": valid}

# ======================================================
# SEND MESSAGE
# ======================================================

@app.post("/send_message")
def send_message(req: MessageRequest):

    # ==================================================
    # ENTROPY SELECTION
    # ==================================================

    if req.commit_id:
        data = reveal_commit(req.commit_id)

        if not data:
            raise HTTPException(400, "Invalid commit ID or expired")

        entropy_hex = data["entropy"]
        secret = data["secret"]
        commit_hash = data["commit"]

        # Verify integrity
        if not verify_commit(entropy_hex, secret, commit_hash):
            raise HTTPException(400, "Commit verification failed")

        print("[Commit-Reveal] Using VERIFIED committed entropy")

        # 🔥 Mark as used (prevents replay)
        mark_commit_used(req.commit_id)

    else:
        entropy_hex = mix_entropy()
        print("[Commit-Reveal] Using LIVE entropy")

    # ==================================================
    # KEY GENERATION
    # ==================================================

    entropy_bytes = bytes.fromhex(entropy_hex)
    combined_entropy = hashlib.sha256(entropy_bytes).digest()

    key = derive_aes_key(combined_entropy)

    full_key_hash = hashlib.sha256(key).hexdigest()
    key_fingerprint = full_key_hash[:16]

    # ==================================================
    # ENCRYPTION
    # ==================================================

    nonce, ciphertext = encrypt_message(key, req.message)

    # ==================================================
    # STORE MESSAGE
    # ==================================================

    CHAT_ROOMS.setdefault(req.roomId, []).append({
        "sender": req.senderId,
        "text": req.message,
        "ts": time.time()
    })

    # ==================================================
    # LOGGING
    # ==================================================

    print("\n" + "=" * 92)
    print("[EntropyLane] 🔐 HYBRID ENTROPY ENCRYPTION")
    print(f"[Room]        : {req.roomId}")
    print(f"[Sender]      : {req.senderId}")
    print("-" * 92)

    print("[Entropy]")
    print("  Source        : Multi-source live system")
    print("  Components    : Traffic + Quantum + Wiki + CPU Jitter")
    print(f"  Mode          : {'Commit-Reveal' if req.commit_id else 'Live'}")

    print("-" * 92)

    print("[Cryptography]")
    print("  Algorithm     : AES-256-GCM")
    print(f"  Key Hash      : {full_key_hash}")
    print(f"  Fingerprint   : {key_fingerprint}")
    print(f"  Nonce         : {nonce.hex()}")
    print(f"  Ciphertext    : {ciphertext.hex()}")

    print("=" * 92 + "\n")

    return {
        "status": "ok",
        "mode": "commit-reveal" if req.commit_id else "live",
        "encrypted": ciphertext.hex(),
        "nonce": nonce.hex(),
        "key_fingerprint": key_fingerprint
    }

# ======================================================
# RECEIVE MESSAGE
# ======================================================

@app.get("/receive_message")
def receive_message(roomId: str, clientId: str, lastTs: float = 0):
    messages = CHAT_ROOMS.get(roomId, [])

    new_messages = [
        m for m in messages
        if m["sender"] != clientId and m["ts"] > lastTs
    ]

    return {"messages": new_messages}