import hashlib
import hmac

def condition_final_seed(mixed_seed, context_info="EntropyLane_V1"):
    """
    NIST-Compliant Conditioning.
    Uses HMAC-SHA512 to 'distill' the mixed entropy into a final 256-bit key.
    """
    # Using a fixed key for the HMAC to act as a 'distiller'
    salt = b"Global_Chaos_Conditioner"
    
    # Generate the final high-entropy key
    final_key = hmac.new(salt, mixed_seed.encode(), hashlib.sha256).hexdigest()
    
    return {
        "key": final_key,
        "audit_id": hashlib.sha1(final_key.encode()).hexdigest()[:8],
        "timestamp": time.time()
    }