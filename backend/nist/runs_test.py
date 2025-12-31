import math

def runs_test(bitstream):
    n = len(bitstream)
    ones = bitstream.count('1')

    pi = ones / n
    if abs(pi - 0.5) >= (2 / math.sqrt(n)):
        return {
            "p_value": 0.0,
            "passed": False
        }

    runs = 1
    for i in range(1, n):
        if bitstream[i] != bitstream[i-1]:
            runs += 1

    numerator = abs(runs - (2 * n * pi * (1 - pi)))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)

    p_value = math.erfc(numerator / denominator)

    return {
        "runs": runs,
        "p_value": p_value,
        "passed": p_value >= 0.01
    }
