import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    grid: list[list[bool]] = []
    trampolines = []
    for y, line in enumerate(lines):
        row = []
        x = 0
        for char in line:
            if char == "#":
                row.append(False)
                x += 1
            elif char == "T":
                row.append(True)
                trampolines.append((x, y))
                x += 1
        grid.append(row)
    seen_jumpable = {}
    for trampoline in trampolines:
        neighbours = get_neighbours(trampoline[0], trampoline[1], grid)
        for neighbour in neighbours:
            smaller = min(trampoline, neighbour)
            larger = max(trampoline, neighbour)
            if smaller not in seen_jumpable:
                seen_jumpable[smaller] = set()
            if larger not in seen_jumpable[smaller]:
                seen_jumpable[smaller].add(larger)
    total = 0
    for key in seen_jumpable:
        total += len(seen_jumpable[key])
    print(total)


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
