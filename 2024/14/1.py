import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    moves = [(l[0], int(l[1:])) for l in lines[0].split(",")]
    total = 0
    maxHeight = 0
    for m in moves:
        if m[0] == "U":
            total += m[1]
        elif m[0] == "D":
            total -= m[1]
        maxHeight = max(maxHeight, total)
    print(maxHeight)

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
