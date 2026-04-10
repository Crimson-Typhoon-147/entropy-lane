import hashlib
from entropy.entropy_mixer import mix_entropy


def generate_aes_key():
    entropy = mix_entropy()

    # Convert to 32-byte key (AES-256)
    key = hashlib.sha256(entropy.encode()).digest()

    return key


if __name__ == "__main__":
    key = generate_aes_key()
    print("Key:", key)
    print("Length:", len(key))
