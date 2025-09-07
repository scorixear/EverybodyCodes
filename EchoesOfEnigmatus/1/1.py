import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i1.txt"), "r", encoding="utf-8") as f:
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
def eni(N, EXP, MOD):
    curr = 1
    remainders = []
    for i in range(EXP):
        curr = (curr * N) % MOD
        remainders.append(curr)
    return int("".join(str(x) for x in remainders[::-1]))

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
