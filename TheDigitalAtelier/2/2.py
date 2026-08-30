import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    start = parse_line(lines[0])
    a = parse_line(lines[1])
    b = parse_line(lines[2])
    c = parse_line(lines[3])
    moves = lines[4].split("=")[1]

    positions = set()
    positions.add(start)
    current = start
    for move in moves:
        target = a
        if move == "A":
            target = a
        elif move == "B":
            target = b
        elif move == "C":
            target = c
        x_diff = (target[0] - current[0]) / 2
        new_x = current[0] + x_diff
        if new_x < 0 and int(new_x) != new_x:
            new_x = int(new_x) - 1
        else:
            new_x = int(new_x)
        y_diff = (target[1] - current[1]) / 2
        new_y = current[1] + y_diff
        if new_y < 0 and int(new_y) != new_y:
            new_y = int(new_y) - 1
        else:
            new_y = int(new_y)
        current = (new_x, new_y)
        positions.add(current)
    fireflies = set()
    for pos in positions:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (pos[0] + dx, pos[1] + dy) not in positions:
                fireflies.add((pos[0] + dx, pos[1] + dy))
    print(len(fireflies))
    print_grid(start, a, b, c, positions, fireflies)


def parse_line(line: str):
    parts = line.split("=")[1][1:-1].split(",")
    return (int(parts[0]), int(parts[1]))


def print_grid(
    start: tuple[int, int],
    a: tuple[int, int],
    b: tuple[int, int],
    c: tuple[int, int],
    positions: set[tuple[int, int]],
    fireflies: set[tuple[int, int]],
):
    max_x = max(
        max(start[0], a[0], b[0], c[0]),
        max(x[0] for x in positions),
        max(x[0] for x in fireflies),
    )
    min_x = min(
        min(start[0], a[0], b[0], c[0]),
        min(x[0] for x in positions),
        min(x[0] for x in fireflies),
    )
    max_y = max(
        max(start[1], a[1], b[1], c[1]),
        max(x[1] for x in positions),
        max(x[1] for x in fireflies),
    )
    min_y = min(
        min(start[1], a[1], b[1], c[1]),
        min(x[1] for x in positions),
        min(x[1] for x in fireflies),
    )

    for y in range(max_y, min_y - 1, -1):
        line = ""
        for x in range(min_x, max_x + 1):
            # if a == (x, y):
            #     line += "A"
            # elif b == (x, y):
            #     line += "B"
            # elif c == (x, y):
            #     line += "C"
            if (x, y) in positions:
                line += "X"
            elif (x, y) in fireflies:
                line += "F"
            else:
                line += "."
        print(line)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
