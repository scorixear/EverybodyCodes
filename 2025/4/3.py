import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    gears = []
    for line in lines:
        if '|' in  line:
            parts = line.split('|')
            gears.append((int(parts[0]), int(parts[1])))
        else:
            gears.append((int(line), int(line)))
    curr_ratio = 1
    for i in range(len(gears) - 1):
        g1r1, g1r2 = gears[i]
        g2r1, g2r2 = gears[i + 1]
        curr_ratio *= (g1r2 / g2r1)
    target = 100
    print(int(target * curr_ratio))
if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
