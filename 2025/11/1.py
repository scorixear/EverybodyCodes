import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    nums = [int(x) for x in lines]
    checksum = duck_sort(nums, 10)
    print(checksum)


def duck_sort(nums, check):
    hasMoved = True
    round_counter = 0
    while hasMoved:
        hasMoved = False
        for i in range(len(nums) - 1):
            if nums[i] > nums[i + 1]:
                nums[i] -= 1
                nums[i + 1] += 1
                hasMoved = True
        if round_counter == check:
            return checksum_calc(nums)
        round_counter += 1
    hasMoved = True
    while hasMoved:
        hasMoved = False
        for i in range(len(nums) - 1):
            if nums[i] < nums[i + 1]:
                nums[i] += 1
                nums[i + 1] -= 1
                hasMoved = True
        if round_counter == check:
            return checksum_calc(nums)
        round_counter += 1
    return 0


def checksum_calc(nums):
    total = 0
    for i, n in enumerate(nums):
        total += (i + 1) * n
    return total


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
