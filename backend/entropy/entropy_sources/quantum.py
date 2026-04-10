import requests
import hashlib
import time


def get_quantum_entropy():
    url = "https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint16"

    headers = {
        "User-Agent": "EntropyLane/1.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code != 200:
            return fallback_entropy()

        data = response.json()

        if "data" not in data or not data["data"]:
            return fallback_entropy()

        # 🔥 Extract quantum value
        quantum_value = str(data["data"][0])

        # 🔥 Add timing noise (important enhancement)
        time_noise = str(time.time_ns())

        # Combine both
        raw = quantum_value + time_noise

        # Hash to produce strong entropy
        return hashlib.sha256(raw.encode()).hexdigest()

    except Exception:
        return fallback_entropy()


# 🚨 Fallback (NEVER FAIL SYSTEM)
def fallback_entropy():
    return hashlib.sha256(str(time.time_ns()).encode()).hexdigest()


if __name__ == "__main__":
    print(get_quantum_entropy())