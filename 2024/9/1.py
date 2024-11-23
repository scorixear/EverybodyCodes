import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    sparkballs = [int(line) for line in lines]
    stamps = [10, 5, 3, 1]
    total = 0
    # greedy approach, always choose the biggest first
    for sparkball in sparkballs:
        brightness = 0
        beetles = 0
        while brightness != sparkball:
            for stamp in stamps:
                if brightness + stamp <= sparkball:
                    brightness += stamp
                    beetles += 1
                    break
        total += beetles
    print(total)

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
