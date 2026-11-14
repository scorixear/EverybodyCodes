import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        grid = text.split("\n")
    seen: set[tuple[int, int]] = set()
    bindings: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    width = len(grid[0])
    height = len(grid)
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if (x, y) in seen:
                continue
            bindings |= flood_fill(x, y, grid, width, height, seen)
    print(len(bindings))


def flood_fill(
    sx: int,
    sy: int,
    grid: list[str],
    width: int,
    height: int,
    seen: set[tuple[int, int]],
) -> set[tuple[tuple[int, int], tuple[int, int]]]:
    border: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    char = grid[sy][sx]
    queue = [(sx, sy)]
    while queue:
        x, y = queue.pop(0)
        if (x, y) in seen:
            continue
        seen.add((x, y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= width:
                border.add(((nx, ny), (-1, -1)))
            elif ny < 0 or ny >= height:
                border.add(((nx, ny), (-2, -2)))
            elif grid[ny][nx] != char:
                if nx < x or ny < y:
                    border.add(((nx, ny), (x, y)))
                else:
                    border.add(((x, y), (nx, ny)))
            else:
                queue.append((nx, ny))
    return border


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
