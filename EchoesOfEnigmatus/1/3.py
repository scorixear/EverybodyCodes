import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
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
def eni(N: int, EXP: int, MOD: int):
    curr = 1
    seen = set()
    seen_list = [curr]
    while curr not in seen:
        seen.add(curr)
        curr = (curr * N) % MOD
        seen_list.append(curr)
    cycle_start = seen_list.index(curr)
    cycle_end = len(seen_list) - 1
    cycle_sum = sum(seen_list[cycle_start+1:])
    cycle_size= cycle_end - cycle_start
    reps, rexp = divmod(EXP - cycle_start, cycle_size)
    return sum(seen_list[1:cycle_start + 1]) + reps * cycle_sum + sum(seen_list[cycle_start + 1: cycle_start + 1 + rexp])  

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
