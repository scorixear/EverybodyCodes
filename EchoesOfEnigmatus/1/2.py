import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    result = 0
    for line in lines:
        parts = line.split(" ")
        A = int(parts[0].split("=")[1])
        B = int(parts[1].split("=")[1])
        C = int(parts[2].split("=")[1])
        X = int(parts[3].split("=")[1])
        Y = int(parts[4].split("=")[1])
        Z = int(parts[5].split("=")[1])
        M = int(parts[6].split("=")[1])
        temp = eni(A, X, M) + eni(B, Y, M) + eni(C, Z, M)
        result = max(result, temp)
    print(result)
def eni(base, exponent, modulus):
    result = ""
    for i in range(5):
        val = pow_mod(base, exponent - i, modulus)
        result += str(val)
    return int(result)

def pow_mod(base, exponent, modulus):
    """Compute (base ** exponent) % modulus using exponentiation by squaring."""
    result = 1
    base = base % modulus
    while exponent > 0:
        if (exponent % 2) == 1:  # If exponent is odd, multiply base with result
            result = (result * base) % modulus
        exponent = exponent >> 1  # Divide exponent by 2
        base = (base * base) % modulus  # Square the base
    return result

def print_overwrite(text):
    """Print text to the console, overwriting the previous line."""
    print(text, end='\r', flush=True)
if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
