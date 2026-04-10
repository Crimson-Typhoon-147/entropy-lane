import hashlib
import time
import uuid
from entropy.entropy_mixer import mix_entropy

# ======================================================
# STORES
# ======================================================

COMMITS = {}          # Active commits
ARCHIVED_COMMITS = {} # For logging / future blockchain

# ⏳ Expiry time (seconds)
COMMIT_TTL = 60


# ======================================================
# CREATE COMMIT
# ======================================================

def create_commit():
    entropy = mix_entropy()
    secret = str(time.time_ns())

    combined = entropy + secret
    commit_hash = hashlib.sha256(combined.encode()).hexdigest()

    commit_id = str(uuid.uuid4())

    COMMITS[commit_id] = {
        "entropy": entropy,
        "secret": secret,
        "commit": commit_hash,
        "timestamp": time.time(),
        "used": False
    }

    return commit_id, commit_hash


# ======================================================
# REVEAL COMMIT
# ======================================================

def reveal_commit(commit_id):

    if commit_id not in COMMITS:
        return None

    data = COMMITS[commit_id]

    # ⏳ Expiry check
    if time.time() - data["timestamp"] > COMMIT_TTL:
        # Move to archive before removing
        ARCHIVED_COMMITS[commit_id] = data
        del COMMITS[commit_id]
        return None

    return data


# ======================================================
# VERIFY COMMIT
# ======================================================

def verify_commit(entropy, secret, commit_hash):
    calculated = hashlib.sha256((entropy + secret).encode()).hexdigest()
    return calculated == commit_hash


# ======================================================
# MARK COMMIT AS USED (ONE-TIME USE)
# ======================================================

def mark_commit_used(commit_id):

    if commit_id not in COMMITS:
        return

    data = COMMITS[commit_id]

    # Mark as used
    data["used"] = True

    # Move to archive (for logs / blockchain later)
    ARCHIVED_COMMITS[commit_id] = data

    # Remove from active pool
    del COMMITS[commit_id]