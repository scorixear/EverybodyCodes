import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    clockwise_numbers = []
    counterclockwise_numbers = []
    for i, n in enumerate(lines):
        parts = n.split("-")
        left = int(parts[0])
        right = int(parts[1])
        if i % 2 == 0:
            for x in range(left, right + 1):
                clockwise_numbers.append(x)
        else:
            for x in range(left, right + 1):
                counterclockwise_numbers.append(x)
    numbers = [1] + clockwise_numbers + counterclockwise_numbers[::-1]
    print(numbers[202520252025 % len(numbers)])


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
