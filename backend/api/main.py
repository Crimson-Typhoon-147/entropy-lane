import hashlib
import time
import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 🛠️ DYNAMIC PATH INJECTION
# This ensures sub-modules (entropy, crypto) are found even if running from different folders
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# 🔥 Core Protocol Imports
from entropy.entropy_mixer import mix_entropy
from entropy.commit_reveal import create_commit, reveal_and_verify
from crypto.aes_gcm import encrypt_message
from crypto.key_derivation import derive_aes_key
from crypto.attestation import attestor  

# ======================================================
# FASTAPI CONFIGURATION
# ======================================================

app = FastAPI(title="EntropyLane Backend", version="1.1.0")

# 🛡️ CORS FIX: Essential for Cloudflare/Localhost interoperability
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store: { "room_id": [list_of_messages] }
CHAT_ROOMS = {}

class MessageRequest(BaseModel):
    roomId: str
    senderId: str
    message: str
    commit_id: str | None = None

# ======================================================
# PROTOCOL ENDPOINTS
# ======================================================

@app.post("/commit")
def commit_entropy():
    try:
        commit_id, commit_hash = create_commit()
        return {"status": "success", "commit_id": commit_id, "commit_hash": commit_hash}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Entropy Error: {str(e)}")

@app.get("/reveal/{commit_id}")
def reveal_entropy(commit_id: str):
    seed, status = reveal_and_verify(commit_id)
    if not seed:
        raise HTTPException(status_code=400, detail=status)
    
    zkp_bundle = attestor.generate_zkp(seed, commit_id)
    proof_packet = {"commit_id": commit_id, "zkp": zkp_bundle, "timestamp": time.time()}
    signature = attestor.sign_bundle(proof_packet)
    
    return {
        "status": "revealed", 
        "entropy": seed, 
        "verification": status,
        "attestation": {
            "zkp": zkp_bundle,
            "signature": signature,
            "public_key": attestor.get_public_key_hex()
        }
    }

# ======================================================
# SYNCED MESSAGING ENDPOINTS
# ======================================================

@app.post("/send_message")
def send_message(req: MessageRequest):
    proof_data = None
    
    if req.commit_id:
        entropy_hex, status = reveal_and_verify(req.commit_id)
        if not entropy_hex:
            raise HTTPException(status_code=400, detail=f"Commit Error: {status}")
        
        zkp = attestor.generate_zkp(entropy_hex, req.commit_id)
        sig = attestor.sign_bundle({"commit_id": req.commit_id, "zkp": zkp})
        proof_data = {"zkp": zkp, "signature": sig}
        mode = "commit-reveal"
    else:
        entropy_hex = mix_entropy()
        mode = "live"

    try:
        entropy_bytes = bytes.fromhex(entropy_hex)
        raw_seed = hashlib.sha256(entropy_bytes).digest()
        key = derive_aes_key(raw_seed)
        key_fingerprint = hashlib.sha256(key).hexdigest()[:16]
        # Store message
        nonce, ciphertext = encrypt_message(key, req.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crypto Error: {str(e)}")

    # USE FLOAT TIMESTAMP FOR FRONTEND FILTERING
    current_ts = float(time.time())
    
    msg_entry = {
        "sender": req.senderId,
        "text": req.message,
        "ts": current_ts, 
        "mode": mode,
        "key_fingerprint": key_fingerprint,
        "proofs": proof_data
    }
    
    if req.roomId not in CHAT_ROOMS:
        CHAT_ROOMS[req.roomId] = []
    
    CHAT_ROOMS[req.roomId].append(msg_entry)
    print(f"✅ [{mode.upper()}] Msg from {req.senderId} stored at {current_ts}")
    
    return {"status": "ok", "timestamp": msg_entry["ts"]}

@app.get("/receive_messages/{roomId}")
def get_messages(roomId: str, clientId: str, lastTs: float = 0.0):
    all_msgs = CHAT_ROOMS.get(roomId, [])
    
    # FILTER: Exclude self, include only newer than lastTs
    new_msgs = [
        m for m in all_msgs 
        if float(m["ts"]) > float(lastTs) and m["sender"] != clientId
    ]
    
    if new_msgs:
        print(f"📡 SYNC: Pushing {len(new_msgs)} messages to {clientId}")
    
    return {"messages": new_msgs}

@app.get("/system/public_key")
def get_server_public_key():
    return {"public_key": attestor.get_public_key_hex()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)