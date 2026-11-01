import os, sys
import time

GREEN = "\033[32m"
GREY = "\033[90m"
YELLOW = "\033[33m"
RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"

Cell = tuple[int, int]
Grid = list[list[int]]

NEIGHBOURS_8 = [
    (dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0)
]

NEIGHBOURS_16 = [
    (dx, dy)
    for dx in (-2, -1, 0, 1, 2)
    for dy in (-2, -1, 0, 1, 2)
    if (dx, dy) != (0, 0)
]


def parse(filename: str = "i3.txt") -> Grid:
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
    grid: Grid, start: Cell, threshold: int = 5, offsets=NEIGHBOURS_8
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
        queue = new_queue
        land_fills |= new_land_fills
    return land_fills


def replace_sand(grid: Grid, land_fills: set[Cell]) -> set[Cell]:
    """Replace land tiles with sand, if there are >= 5 water tiles around them."""
    sand_tiles = set()
    for x, y in land_fills:
        if (x, y) in sand_tiles:
            continue
        around = neighbours(grid, (x, y))
        count = 8 - len(around)
        for nx, ny in around:
            if (nx, ny) not in land_fills:
                count += 1
        if count >= 1:
            sand_tiles.add((x, y))
    newly_added = True
    while newly_added:
        newly_added = False
        for x, y in land_fills:
            if (x, y) in sand_tiles:
                continue
            around = neighbours(grid, (x, y))
            count = 0
            for nx, ny in around:
                if (nx, ny) in sand_tiles:
                    count += 1
            if count >= 5:
                sand_tiles.add((x, y))
                newly_added = True
    return sand_tiles


def replace_trees(
    grid: Grid, land_fills: set[Cell], sand_tiles: set[Cell]
) -> set[Cell]:
    """Replaces land tiles with trees if 1. Pattern matches. Then simulate two generations, where 4 neighbours are trees and none are sand."""
    tree_tiles = set()
    for x, y in land_fills:
        if (x, y) in tree_tiles:
            continue
        around = neighbours(grid, (x, y), offsets=NEIGHBOURS_16)
        around.remove((x - 2, y - 2))
        around.remove((x + 2, y - 2))
        around.remove((x - 2, y + 2))
        around.remove((x + 2, y + 2))
        all_land = all((nx, ny) in land_fills for nx, ny in around)
        if all_land:
            tree_tiles.add((x, y))
    for i in range(2):
        new_tree_tiles = set()
        for x, y in land_fills:
            if (x, y) in tree_tiles:
                continue
            around = neighbours(grid, (x, y), offsets=NEIGHBOURS_8)
            has_sand = any((nx, ny) in sand_tiles for nx, ny in around)
            if has_sand:
                continue
            count = sum(1 for nx, ny in around if (nx, ny) in tree_tiles)
            if count >= 4:
                new_tree_tiles.add((x, y))
        tree_tiles |= new_tree_tiles
    return tree_tiles


def solve(grid: Grid) -> int:
    start = (len(grid[0]) // 2, len(grid) // 2)
    land_fills = fill_land(grid, start)
    print_grid(grid, land_fills, set(), set())
    sand_tiles = replace_sand(grid, land_fills)
    print_grid(grid, land_fills, sand_tiles, set())
    land_fills -= sand_tiles
    tree_tiles = replace_trees(grid, land_fills, sand_tiles)
    print_grid(grid, land_fills, sand_tiles, tree_tiles)
    return len(tree_tiles)


def main():
    print(solve(parse()))


def print_grid(
    grid: Grid, land_fills: set[Cell], sand_tiles: set[Cell], tree_tiles: set[Cell]
):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x, y) in sand_tiles:
                print(f"{YELLOW}={RESET}", end="")
                continue
            if (x, y) in tree_tiles:
                print(f"{RED}@{RESET}", end="")
                continue
            if (x, y) in land_fills:
                print(f"{GREEN}#{RESET}", end="")
                continue
            print(f"{BLUE}.{RESET}", end="")
        print()
    print("")


if __name__ == "__main__":
    if os.name == "nt":
        os.system("")  # enables ANSI escape code processing in the Windows console
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
