from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def encrypt_message(key, plaintext):
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 96-bit nonce
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
    return nonce, ciphertext

def decrypt_message(key, nonce, ciphertext):
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode()
