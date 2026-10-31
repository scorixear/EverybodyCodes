import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    total = 0
    for line in lines:
        left, right = line.split(" ")
        iso = left.split("-")[1]
        char_count = len(right)
        result = 0
        for i in range(char_count - 1, -1, -1):
            iso_c = int(iso[mod_iso(i, iso, char_count)])
            vote_c = int(right[i])
            result += vote_c * (iso_c ** (char_count - i - 1))
        total += result
    print(total)


def mod_iso(i: int, iso: str, char_count: int):
    a = char_count - i - 1
    b = a % len(iso)
    c = len(iso) - b
    d = c - 1
    return d


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
