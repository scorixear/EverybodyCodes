import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    total = 0
    for line in lines:
        jumps = [int(x) for x in line.split(",")]
        total += recaman(jumps)
    print(total)


def recaman(jumps: list[int]):
    current = 0
    seen = {0}
    for j in jumps:
        if current - j >= 0 and (current - j) not in seen:
            current -= j
            seen.add(current)
        else:
            while (current + j) in seen:
                j += 1
            current += j
            seen.add(current)
    return current


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
