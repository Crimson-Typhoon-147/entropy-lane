from crypto.entropy_key import generate_aes_key
from crypto.aes_crypto import encrypt_message, decrypt_message

key = generate_aes_key()

message = "Hello EntropyLane 🚀"

enc = encrypt_message(message, key)
dec = decrypt_message(enc, key)

print("Encrypted:", enc)
print("Decrypted:", dec)
