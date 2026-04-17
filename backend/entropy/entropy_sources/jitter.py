import time
import hashlib
import os

def get_jitter_entropy():
    """
    Captures CPU timing jitter caused by background noise and thermal variance.
    """
    entropy_bits = []
    
    for _ in range(64):
        t1 = time.perf_counter_ns()
        # Perform actual work to prevent compiler optimization
        x = 0
        for i in range(500):
            x += (i ^ (i-1))
        t2 = time.perf_counter_ns()
        
        # We only care about the least significant bits of the difference
        delta = t2 - t1
        entropy_bits.append(str(delta % 2)) # Capture bit-level flip-flops
        
    raw_data = "".join(entropy_bits) + str(os.getpid())
    return hashlib.sha256(raw_data.encode()).hexdigest()

if __name__ == "__main__":
    print("Jitter Oracle Output:", get_jitter_entropy())