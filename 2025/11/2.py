import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "e2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    nums = [int(x) for x in lines]
    counter = duck_sort(nums)
    print(counter - 2)


def duck_sort(nums):
    hasMoved = True
    round_counter = 0
    while hasMoved:
        hasMoved = False
        for i in range(len(nums) - 1):
            if nums[i] > nums[i + 1]:
                nums[i] -= 1
                nums[i + 1] += 1
                hasMoved = True
        round_counter += 1
        print(nums)
    hasMoved = True
    while hasMoved:
        hasMoved = False
        for i in range(len(nums) - 1):
            if nums[i] < nums[i + 1]:
                nums[i] += 1
                nums[i + 1] -= 1
                hasMoved = True
        round_counter += 1
        print(nums)
    return round_counter


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
