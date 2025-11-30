import os, sys
import time
import dijkstra


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
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
    if x > 0 and grid[y][x - 1]:
        neighbours.append((x - 1, y))
    # right
    if x < len(grid[y]) - 1 and grid[y][x + 1]:
        neighbours.append((x + 1, y))
    # top
    if facing and y > 0 and x < len(grid[y - 1]) - 1 and grid[y - 1][x + 1]:
        neighbours.append((x + 1, y - 1))
    # bottom
    if not facing and y < len(grid) - 1 and x > 0 and grid[y + 1][x - 1]:
        neighbours.append((x - 1, y + 1))

    return neighbours


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
