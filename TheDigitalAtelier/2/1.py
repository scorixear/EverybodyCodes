import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
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
    print(len(positions))
    print_grid(start, a, b, c, positions)


def parse_line(line: str):
    parts = line.split("=")[1][1:-1].split(",")
    return (int(parts[0]), int(parts[1]))


def print_grid(
    start: tuple[int, int],
    a: tuple[int, int],
    b: tuple[int, int],
    c: tuple[int, int],
    positions: set[tuple[int, int]],
):
    max_x = max(start[0], a[0], b[0], c[0])
    min_x = min(start[0], a[0], b[0], c[0])
    max_y = max(start[1], a[1], b[1], c[1])
    min_y = min(start[1], a[1], b[1], c[1])

    for y in range(max_x, min_x - 1, -1):
        line = ""
        for x in range(min_x, max_x + 1):
            if a == (x, y):
                line += "A"
            elif b == (x, y):
                line += "B"
            elif c == (x, y):
                line += "C"
            elif (x, y) in positions:
                line += "X"
            else:
                line += "."
        print(line)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
