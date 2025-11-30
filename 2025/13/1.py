import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    numbers = [0] * (len(lines) + 1)
    inserts = [1] + [int(line) for line in lines]
    for i, n in enumerate(inserts):
        if i % 2 == 1:
            numbers[i // 2 + 1] = n
        else:
            numbers[-(i // 2)] = n
    print(numbers[2025 % len(numbers)])


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
