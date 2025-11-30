import os, sys
import time
import math


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    grid = []
    volcano = (0, 0)
    for i, line in enumerate(lines):
        row = []
        for j, char in enumerate(line):
            if char == "@":
                row.append(0)
                volcano = (j, i)
            else:
                row.append(int(char))
        grid.append(row)

    destroyed_per_radius = {}
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x, y) == volcano:
                continue
            dist = math.ceil(math.sqrt((volcano[0] - x) ** 2 + (volcano[1] - y) ** 2))
            if dist not in destroyed_per_radius:
                destroyed_per_radius[dist] = 0
            destroyed_per_radius[dist] += grid[y][x]
    max_destroyed = 0
    max_radius = 0
    for r in destroyed_per_radius:
        if destroyed_per_radius[r] > max_destroyed:
            max_destroyed = destroyed_per_radius[r]
            max_radius = r

    print(max_radius * max_destroyed)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
