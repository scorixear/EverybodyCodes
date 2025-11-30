import os, sys
import time
import math
import dijkstra


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    grid: list[list[bool]] = []
    start = (0, 0)
    end = (0, 0)
    for y, line in enumerate(lines):
        row = []
        x = 0
        for char in line:
            if char == "#":
                row.append(False)
                x += 1
            elif char == "T":
                row.append(True)
                x += 1
            elif char == "S":
                row.append(True)
                start = (x, y)
                x += 1
            elif char == "E":
                row.append(True)
                end = (x, y)
                x += 1
        grid.append(row)

    algo = dijkstra.Dijkstra(
        lambda pos: get_neighbours(pos[0], pos[1], grid), lambda a, b: 1, 0
    )
    algo.find_path(start, end)
    cost = algo.get_cost(end)
    print(cost)


def get_neighbours(x: int, y: int, grid: list[list[bool]]) -> list[tuple[int, int]]:
    neighbours = []
    facing = x % 2 == 0
    # left
    if x > 0:
        nx, ny = translate_rotation(x - 1, y, grid)
        if grid[ny][nx]:
            neighbours.append((nx, ny))
    # right
    if x < len(grid[y]) - 1:
        nx, ny = translate_rotation(x + 1, y, grid)
        if grid[ny][nx]:
            neighbours.append((nx, ny))
    # top
    if facing and y > 0 and x < len(grid[y - 1]) - 1:
        nx, ny = translate_rotation(x + 1, y - 1, grid)
        if grid[ny][nx]:
            neighbours.append((nx, ny))
    # bottom
    if not facing and y < len(grid) - 1 and x > 0:
        nx, ny = translate_rotation(x - 1, y + 1, grid)
        if grid[ny][nx]:
            neighbours.append((nx, ny))

    # same place
    nx, ny = translate_rotation(x, y, grid)
    if grid[ny][nx]:
        neighbours.append((nx, ny))
    return neighbours


def translate_rotation(x: int, y: int, grid: list[list[bool]]) -> tuple[int, int]:
    max_y = len(grid) - 1
    ny = max_y - y - math.ceil(x / 2)
    nx = len(grid[ny]) - 1 - x
    return (nx, ny)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
