import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
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

    radius = 10
    total = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x, y) == volcano:
                continue
            dist = (volcano[0] - x) ** 2 + (volcano[1] - y) ** 2
            if dist <= radius**2:
                total += grid[y][x]
    print(total)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
