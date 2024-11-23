import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    sparkballs = [int(line) for line in lines]
    stamps = [1, 3, 5, 10, 15, 16, 20, 24, 25, 30, 37, 38, 49, 50, 74, 75, 100, 101]
    
    # iterative dp approach, precompute all possible sparkballs
    total = 0
    max_sparkball = max(sparkballs)
    dp = [float('inf')] * (max_sparkball + 1)
    dp[0] = 0
    for x in range(1, max_sparkball+1):
        for stamp in stamps:
            if x >= stamp:
                dp[x] = min(dp[x], dp[x - stamp] + 1)
    
    for sparkball in sparkballs:
        min_sparkball = float("inf")
        lower = sparkball // 2
        higher = sparkball // 2
        if sparkball % 2 == 1:
            higher += 1
        for split_spark in range(0, 51):
            min_sparkball = min(min_sparkball, dp[lower + split_spark] + dp[higher - split_spark])
        total += min_sparkball
    print(total)

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
