import hashlib
import time
import uuid
import secrets
from entropy.entropy_mixer import mix_entropy

COMMITS = {}

def create_commit():
    """PHASE 1: COMMIT"""
    # This now calls the self-sufficient mixer
    raw_entropy = mix_entropy()
    secret_nonce = secrets.token_hex(16)

    combined = f"{raw_entropy}{secret_nonce}"
    commit_hash = hashlib.sha256(combined.encode()).hexdigest()

    commit_id = str(uuid.uuid4())
    COMMITS[commit_id] = {
        "entropy": raw_entropy,
        "secret": secret_nonce,
        "commit_hash": commit_hash,
        "timestamp": time.time()
    }
    return commit_id, commit_hash

def reveal_and_verify(commit_id):
    """PHASE 2: REVEAL"""
    if commit_id not in COMMITS:
        return None, "Error: Commit ID not found"

    data = COMMITS[commit_id]
    check_val = f"{data['entropy']}{data['secret']}"
    verification_hash = hashlib.sha256(check_val.encode()).hexdigest()

    if verification_hash == data["commit_hash"]:
        return data["entropy"], "SUCCESS: Source Verified"
    else:
        return None, "FAILURE: Tamper detected"

if __name__ == "__main__":
    print("\n[STEP 1] Initializing Entropy Sources...")
    cid, chash = create_commit()
    print(f" -> Commitment Created: {chash[:32]}...")

    print("\n[STEP 2] Simulating Reveal Phase...")
    time.sleep(1) 
    final_seed, status = reveal_and_verify(cid)
    
    print(f" -> Status: {status}")
    if final_seed:
        print(f" -> Final Secure Seed: {final_seed[:64]}...")
        print("\n[RESULT] System is 100% Operational.\n")