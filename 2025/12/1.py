import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    grid = [[int(c) for c in line] for line in lines]
    stack = [(0, 0)]
    visited = set()
    while stack:
        x, y = stack.pop(0)
        visited.add((x, y))
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (
                0 <= ny < len(grid)
                and 0 <= nx < len(grid[0])
                and grid[y][x] >= grid[ny][nx]
                and (nx, ny) not in visited
            ):
                stack.append((nx, ny))
    print(len(visited))


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
