from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64


def encrypt_message(message: str, key: bytes):
    cipher = AES.new(key, AES.MODE_GCM)

    ciphertext, tag = cipher.encrypt_and_digest(message.encode())

    return {
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "nonce": base64.b64encode(cipher.nonce).decode(),
        "tag": base64.b64encode(tag).decode()
    }


def decrypt_message(enc_data: dict, key: bytes):
    cipher = AES.new(key, AES.MODE_GCM, nonce=base64.b64decode(enc_data["nonce"]))

    plaintext = cipher.decrypt_and_verify(
        base64.b64decode(enc_data["ciphertext"]),
        base64.b64decode(enc_data["tag"])
    )

    return plaintext.decode()
