# crypto/key_derivation.py

import hashlib

def derive_aes_key(entropy_bytes: bytes, key_size: int = 32) -> bytes:
    """
    Derive a fixed-length AES key from entropy bytes.
    Default: 32 bytes = AES-256
    """
    return hashlib.sha256(entropy_bytes).digest()[:key_size]
