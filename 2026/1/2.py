import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    nums = [int(l) for l in lines[0].split(",")]
    count = 0
    for num in nums:
        x = 3
        while formula(x) < num:
            x += 1
        count += formula(x) - num
    print(count)


def formula(x: int) -> int:
    return 4 * x - 4


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
