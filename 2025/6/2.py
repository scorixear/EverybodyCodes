import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    mentors = {}
    result = 0
    for i, char in enumerate(lines[0]):
        if char.upper() == char:
            mentors[char] = mentors.get(char, 0) + 1
        else:
            result += mentors.get(char.upper(), 0)
    print(result)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
