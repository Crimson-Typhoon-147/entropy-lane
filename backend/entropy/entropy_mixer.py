import hashlib
import logging

# Import your upgraded sources from the subfolder
from entropy.entropy_sources.jitter import get_jitter_entropy
from entropy.entropy_sources.quantum import get_quantum_entropy
from entropy.entropy_sources.wikipedia import get_wiki_entropy
from entropy.entropy_sources.traffic import get_traffic_entropy

def mix_entropy():
    """
    MASTER MIXER: Aggregates entropy from all oracles into a final master seed.
    """
    # 1. Gather raw entropy from all available Oracles
    raw_sources = {
        "jitter": get_jitter_entropy(),
        "quantum": get_quantum_entropy(),
        "wikipedia": get_wiki_entropy(),
        "traffic": get_traffic_entropy()
    }

    # 2. Cryptographic Mixing (SHA-512)
    mixer = hashlib.sha512()
    
    for source_name, value in raw_sources.items():
        if value:
            # Salted mixing: H(source_name + value)
            salted_data = f"{source_name}:{value}".encode()
            mixer.update(salted_data)
        else:
            print(f"⚠️ Warning: Source {source_name} returned no data.")

    return mixer.hexdigest()

if __name__ == "__main__":
    print("--- Testing Master Mixer ---")
    print(mix_entropy())