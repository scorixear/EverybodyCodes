import os, sys
import time

GREEN = "\033[32m"
GREY = "\033[90m"
RESET = "\033[0m"

Cell = tuple[int, int]
Grid = list[list[int]]

NEIGHBOURS_8 = [
    (dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0)
]


def parse(filename: str = "i1.txt") -> Grid:
    with open(os.path.join(sys.path[0], filename), "r", encoding="utf-8") as f:
        lines = f.read().strip().split("\n")
    return [[1 if c == "1" else 0 for c in line] for line in lines]


def neighbours(grid: Grid, cell: Cell, offsets=NEIGHBOURS_8) -> list[Cell]:
    x, y = cell
    return [
        (x + dx, y + dy)
        for dx, dy in offsets
        if 0 <= x + dx < len(grid[0]) and 0 <= y + dy < len(grid)
    ]


def fill_land(
    grid: Grid,
    start: Cell,
    threshold: int = 5,
    offsets=NEIGHBOURS_8,
    debug: bool = False,
) -> set[Cell]:
    """Grow land outwards from start: a cell becomes land once at least
    `threshold` of its neighbours are land (grid value 1 or already filled)."""
    land_fills = {start}
    queue = set(neighbours(grid, start, offsets))
    while queue:
        new_land_fills = set()
        new_queue = set()
        for cell in queue:
            around = neighbours(grid, cell, offsets)
            count = sum(
                1 for nx, ny in around if grid[ny][nx] == 1 or (nx, ny) in land_fills
            )
            if count >= threshold:
                new_land_fills.add(cell)
                new_queue.update(
                    n for n in around if n not in land_fills and n not in new_land_fills
                )
            if debug:
                print_grid(grid, land_fills | new_land_fills, queue | new_queue)
        queue = new_queue
        land_fills |= new_land_fills
    return land_fills


def solve(grid: Grid) -> int:
    start = (len(grid[0]) // 2, len(grid) // 2)
    land_tiles = fill_land(grid, start)
    print_grid(grid, land_tiles, set())
    return len(land_tiles)


def main():
    print(solve(parse()))


def print_grid(grid: Grid, land_fills: set[Cell], queue: set[Cell]):
    os.system("cls" if os.name == "nt" else "clear")
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x, y) in land_fills:
                print(f"{GREEN}#{RESET}", end="")
                continue
            char = str(grid[y][x])
            print(char if (x, y) in queue else f"{GREY}{char}{RESET}", end="")
        print()
    time.sleep(0.1)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
