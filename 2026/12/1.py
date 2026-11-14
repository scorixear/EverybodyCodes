import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    seen: set[tuple[int, int]] = set()
    stacks: list[tuple[int, int]] = []
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == ".":
                continue
            if (x, y) in seen:
                continue
            stacks.append(flood_fill(x, y, lines, seen))
    count = 0
    # print(stacks)
    for stack in stacks:
        if stack[0] < stack[1]:
            count += stack[0]
        else:
            count += stack[1]
    print(count)


def flood_fill(startx, starty, grid, seen) -> tuple[int, int]:
    width = len(grid[0])
    height = len(grid)
    queue = [(startx, starty)]
    min_x = startx
    max_x = startx
    min_y = starty
    max_y = starty
    while queue:
        x, y = queue.pop(0)
        if (x, y) in seen:
            continue
        seen.add((x, y))
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == "#":
                queue.append((nx, ny))
    return (max_x - min_x + 1, max_y - min_y + 1)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
