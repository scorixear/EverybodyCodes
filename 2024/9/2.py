import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    sparkballs = [int(line) for line in lines]
    stamps = [30, 25, 24, 20, 16, 15, 10, 5, 3, 1]
    total = 0
    # dp approach, save previous beetles needed for each sparkball
    for sparkball in sparkballs:
        dp: dict[int, int] = dict()
        total += find_min(stamps, 0, sparkball, dp)
    print(total)

def find_min(stamps: list[int], beetle_count: int, total: int, dp: dict[int, int]) -> int:
    if total == 0:
        return beetle_count
    elif total < 0:
        return float("inf")
    elif total in dp:
        return dp[total]
    else:
        min_beetle_count = float("inf")
        for stamp in stamps:
            min_beetle_count = min(min_beetle_count, find_min(stamps, beetle_count + 1, total - stamp, dp))
        dp[total] = min_beetle_count
        return min_beetle_count

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
