import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    mentors = []
    novices = []
    result = 0
    for i, char in enumerate(lines[0]):
        if char == "A":
            mentors.append(i)
        elif char == "a":
            novices.append(i)
            result += len(mentors)
    print(result)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
