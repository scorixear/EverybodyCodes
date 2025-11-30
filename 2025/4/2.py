import os, sys
import time
import math

def main():
    with open(os.path.join(sys.path[0],"i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    gears = [int(x) for x in lines]
    gear_ratio = gears[0] / gears[-1]
    target_gear = 10000000000000
    print(math.ceil(target_gear / gear_ratio))

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
