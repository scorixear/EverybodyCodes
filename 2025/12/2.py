import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    grid = [[int(c) for c in line] for line in lines]
    stack = set([(0, 0), (len(grid[0]) - 1, len(grid) - 1)])
    visited = set()
    while stack:
        next_stack = set()
        for x, y in stack:
            visited.add((x, y))
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (
                    0 <= ny < len(grid)
                    and 0 <= nx < len(grid[0])
                    and grid[y][x] >= grid[ny][nx]
                    and (nx, ny) not in visited
                ):
                    next_stack.add((nx, ny))
        stack = next_stack
    print(len(visited))


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
