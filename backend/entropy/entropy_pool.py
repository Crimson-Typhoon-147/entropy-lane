import hashlib
import struct

def condition_entropy(entropy_windows):
    """
    Takes entropy windows and produces SHA-256 conditioned entropy blocks.
    """
    conditioned_blocks = []

    for window in entropy_windows:
        data = struct.pack(
            "dd",
            float(window["shannon_entropy"]),
            float(window["min_entropy"])
        )

        digest = hashlib.sha256(data).hexdigest()
        conditioned_blocks.append(digest)

    return conditioned_blocks
