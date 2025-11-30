import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    nums = [int(x) for x in lines[0].split(",")]
    nails = 256
    connections: dict[int, set[int]] = {}
    for i in range(nails + 1):
        connections[i] = set()
    total = 0
    curr = nums[0]
    for num in nums[1:]:
        curr_total = 0
        smaller = min(curr, num)
        larger = max(curr, num)
        for i in range(smaller + 1, larger):
            for con in connections[i]:
                if con < smaller or con > larger:
                    curr_total += 1
        connections[smaller].add(larger)
        connections[larger].add(smaller)
        curr = num
        total += curr_total
    print(total)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
