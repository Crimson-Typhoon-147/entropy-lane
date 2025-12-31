import math

def frequency_test(bitstream):
    n = len(bitstream)
    ones = bitstream.count('1')
    zeros = bitstream.count('0')

    s_obs = abs(ones - zeros) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))

    return {
        "ones": ones,
        "zeros": zeros,
        "p_value": p_value,
        "passed": p_value >= 0.01
    }


