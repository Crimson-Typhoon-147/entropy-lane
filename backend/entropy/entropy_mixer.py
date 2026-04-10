import hashlib

from entropy.entropy_sources.jitter import get_jitter_entropy
from entropy.entropy_sources.quantum import get_quantum_entropy
from entropy.entropy_sources.wikipedia import get_wiki_entropy
from entropy.entropy_sources.traffic import get_traffic_entropy


def mix_entropy():
    sources = [
        get_jitter_entropy(),
        get_quantum_entropy(),
        get_wiki_entropy(),
        get_traffic_entropy()
    ]

    combined = 0

    for s in sources:
        if s:
            combined ^= int(hashlib.sha256(s.encode()).hexdigest(), 16)

    final = hashlib.sha512(str(combined).encode()).hexdigest()

    return final


if __name__ == "__main__":
    print("Final Entropy:\n", mix_entropy())
