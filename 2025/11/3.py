import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    nums = [int(x) for x in lines]
    counter = duck_sort(nums)
    print(counter)


def duck_sort(nums):
    mean = sum(nums) // len(nums)
    return sum(mean - num for num in nums if num < mean)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
