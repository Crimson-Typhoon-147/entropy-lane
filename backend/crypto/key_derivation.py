import hashlib

def derive_key(entropy_blocks, key_size=32):
    """
    Derive a symmetric key from conditioned entropy blocks.
    AES-256 requires 32 bytes.
    """
    combined = "".join(entropy_blocks).encode()
    digest = hashlib.sha256(combined).digest()

    return digest[:key_size]
