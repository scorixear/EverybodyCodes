import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    nums = [int(x) for x in lines[0].split(",")]
    nails = 32
    curr = nums[0]
    total = 0
    for num in nums[1:]:
        if abs(num - curr) == (nails / 2):
            total += 1
        curr = num
    print(total)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
