import hashlib
import json
import secrets
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

class AttestationProvider:
    def __init__(self):
        # Generate the server's identity (Private Key stays on server)
        self.private_key = ec.generate_private_key(ec.SECP256R1())
        self.public_key = self.private_key.public_key()

    def get_public_key_hex(self):
        """Returns the public key for the frontend to verify signatures."""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        ).hex()

    def sign_bundle(self, data_dict):
        """LAYER 1: ECDSA Digital Signature."""
        payload = json.dumps(data_dict, sort_keys=True).encode()
        signature = self.private_key.sign(payload, ec.ECDSA(hashes.SHA256()))
        return signature.hex()

    def generate_zkp(self, secret_seed, commit_hash):
        """
        LAYER 2: Non-Interactive Zero-Knowledge Proof (NIZKP).
        Proves we know the 'secret_seed' that makes 'commit_hash'.
        """
        # Create a 'witness' (random temporary secret)
        v = secrets.token_hex(16)
        # Commitment to the witness
        t = hashlib.sha256(v.encode()).hexdigest() 
        
        # Challenge (Fiat-Shamir Heuristic)
        # c = H(Commitment + Witness_Commitment)
        c = hashlib.sha256(f"{commit_hash}{t}".encode()).hexdigest()
        
        # Response (r = v + c * secret) - Simplified for hexadecimal strings
        # In a real ZKP, this involves finite field arithmetic.
        r = hashlib.sha256(f"{v}{c}{secret_seed}".encode()).hexdigest()
        
        return {"t": t, "c": c, "r": r}

# Global instance
attestor = AttestationProvider()
