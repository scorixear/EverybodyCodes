import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    grid = [[int(c) for c in line] for line in lines]
    max_1, pos_1 = find_max(grid, set())
    max_2, pos_2 = find_max(grid, max_1)
    max_3, pos_3 = find_max(grid, max_2)
    visited = barrel([pos_1, pos_2, pos_3], grid, set())
    print(len(visited))


def find_max(grid, visited: set):
    max_visited = set()
    max_pos = (0, 0)
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x, y) not in visited:
                new_visited = barrel([(x, y)], grid, visited.copy())
                if len(new_visited) > len(max_visited):
                    max_visited = new_visited
                    max_pos = (x, y)
    return max_visited, max_pos


def barrel(start, grid, visited):
    stack = set(start)
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
    return visited


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
