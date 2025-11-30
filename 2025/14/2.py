import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    active_cells = set()
    width = len(lines[0])
    height = len(lines)
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                active_cells.add((x, y))
    total = 0
    for _ in range(2025):
        new_active_cells = set()
        for y in range(0, height):
            for x in range(0, width):
                neighbours = 0
                for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                    nx, ny = x + dx, y + dy
                    if (
                        0 <= nx < width
                        and 0 <= ny < height
                        and (nx, ny) in active_cells
                    ):
                        neighbours += 1
                if (x, y) in active_cells:
                    if neighbours % 2 == 1:
                        new_active_cells.add((x, y))
                elif neighbours % 2 == 0:
                    new_active_cells.add((x, y))
        active_cells = new_active_cells
        total += len(active_cells)
    print(total)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
