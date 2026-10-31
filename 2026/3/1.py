import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    total = 0
    for line in lines:
        left, right = line.split(" ")
        iso = left.split("-")[1]
        char_count = len(iso)
        result = 0
        for i in range(char_count):
            iso_c = int(iso[i])
            vote_c = int(right[i])
            result += vote_c * (iso_c ** (char_count - i - 1))
        total += result
    print(total)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
