import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    pines = set()
    channel = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "P":
                pines.add((x, y))
            elif c == ".":
                channel.add((x, y))
    water = set()
    water.add((0, 1))
    water.add((len(lines[0]) -1, len(lines) - 2))
    channel.remove((0, 1))
    channel.remove((len(lines[0]) -1, len(lines) - 2))
    counter = 0
    while pines:
        to_be_added = set()
        for x, y in water:
            dd = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dx, dy in dd:
                if (x + dx, y + dy) in channel:
                    channel.remove((x + dx, y + dy))
                    to_be_added.add((x + dx, y + dy))
                elif (x + dx, y + dy) in pines:
                    pines.remove((x + dx, y + dy))
                    to_be_added.add((x + dx, y + dy))
        water = to_be_added
        counter += 1
    print(counter)
    

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
