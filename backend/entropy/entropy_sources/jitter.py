import time
import hashlib

def get_jitter_entropy():
    t1 = time.perf_counter_ns()
    
    for _ in range(10000):
        pass
    
    t2 = time.perf_counter_ns()
    
    diff = t2 - t1
    return hashlib.sha256(str(diff).encode()).hexdigest()


if __name__ == "__main__":
    print(get_jitter_entropy())
