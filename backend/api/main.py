import hashlib
import time
import os
import sys
import asyncio
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# 🛠️ PATH FIX
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# 🔥 Imports
from entropy.entropy_mixer import mix_entropy
from crypto.aes_gcm import encrypt_message
from crypto.key_derivation import derive_aes_key

def evaluate_entropy_health(shannon, min_entropy, nist_pass):
    """
    Synchronized Health Check.
    If nist_pass is True from the mixer, we report HEALTHY.
    """
    if nist_pass:
        return {
            "level": "HEALTHY ✅",
            "risk": "Low (Cryptographically Secure)",
            "advice": "Suitable for encryption"
        }
    elif shannon >= 5.0:
        return {
            "level": "MODERATE ⚠️",
            "risk": "Medium (Adequate for demo)",
            "advice": "Stable but check hardware"
        }
    else:
        return {
            "level": "WEAK ❌",
            "risk": "High (Predictable)",
            "advice": "Reject or re-generate entropy"
        }

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CHAT_ROOMS = {}
ACTIVE_CONNECTIONS = {}

class MessageRequest(BaseModel):
    roomId: str
    senderId: str
    senderName: str = Field(..., min_length=1)
    message: str
    commit_id: str | None = None

# ======================================================
# WEBSOCKET & BROADCAST
# ======================================================

async def broadcast(room_id, message):
    if room_id in ACTIVE_CONNECTIONS:
        dead = []
        for connection in ACTIVE_CONNECTIONS[room_id]:
            try:
                await connection.send_json(message)
            except:
                dead.append(connection)
        for d in dead:
            ACTIVE_CONNECTIONS[room_id].remove(d)

@app.websocket("/ws/{room_id}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, client_id: str):
    await websocket.accept()
    ACTIVE_CONNECTIONS.setdefault(room_id, []).append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ACTIVE_CONNECTIONS[room_id].remove(websocket)

# ======================================================
# MESSAGE ENDPOINT
# ======================================================

@app.post("/send_message")
async def send_message(req: MessageRequest):
    if not req.senderName.strip():
        raise HTTPException(status_code=400, detail="Username required")

    # 🔐 CALL MIXER
    entropy_data = mix_entropy()

    # EXTRACT DATA
    entropy_hex = entropy_data["entropy_hex"]
    shannon = entropy_data["shannon_entropy"]
    min_ent = entropy_data["min_entropy"]
    nist_pass = entropy_data["nist_pass"] # Master boolean from mixer
    source = entropy_data["source"]

    # 🔥 SYNCED HEALTH CHECK
    health = evaluate_entropy_health(shannon, min_ent, nist_pass)

    # 🔑 KEY DERIVATION
    entropy_bytes = bytes.fromhex(entropy_hex)
    raw_seed = hashlib.sha256(entropy_bytes).digest()
    key = derive_aes_key(raw_seed)
    key_fingerprint = hashlib.sha256(key).hexdigest()[:16]

    # 🔒 ENCRYPT
    nonce, ciphertext = encrypt_message(key, req.message)
    current_ts = float(time.time())

    msg_entry = {
        "sender": req.senderName,
        "sender_id": req.senderId,
        "text": req.message,
        "ts": current_ts,
        "key_fingerprint": key_fingerprint,
    }

    CHAT_ROOMS.setdefault(req.roomId, []).append(msg_entry)

    # ======================================================
    # 🔥 FINAL STRUCTURED LOG
    # ======================================================
    print("\n" + "="*60)
    print("[EntropyLane] 🔐 SECURE MESSAGE TRANSACTION")
    print("-"*60)
    print(f"[Room]        : {req.roomId}")
    print(f"[Sender]      : {req.senderName} ({req.senderId})")
    
    print("\n[Entropy Analysis]")
    print(f"  Source              : {source}")
    print(f"  Shannon Entropy     : {round(shannon, 4)} bits")
    print(f"  Min-Entropy         : {round(min_ent, 4)} bits")
    print(f"  NIST Status         : {'PASS ✅' if nist_pass else 'FAIL ❌'}")

    print("\n[Entropy Health]")
    print(f"  Quality Level       : {health['level']}")
    print(f"  Risk Assessment     : {health['risk']}")
    print(f"  Recommendation      : {health['advice']}")

    print("\n[Cryptographic Details]")
    print(f"  Algorithm           : AES-256-GCM")
    print(f"  Key Fingerprint     : {key_fingerprint}")
    print(f"  Ciphertext Length   : {len(ciphertext)} bytes")
    print("="*60 + "\n")

    asyncio.create_task(broadcast(req.roomId, msg_entry))
    # Change the last line of send_message in main.py to this:
    return {
    "status": "ok",
    "shannon": shannon,
    "min_entropy": min_ent,
    "nist_pass": nist_pass
    }

@app.get("/receive_messages/{roomId}")
def receive_messages(roomId: str, clientId: str):
    if roomId not in CHAT_ROOMS: return {"messages": []}
    filtered = [msg for msg in CHAT_ROOMS[roomId] if msg.get("sender_id") != clientId]
    return {"messages": filtered}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)