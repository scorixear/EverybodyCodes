import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    size_y = len(lines)
    size_x = len(lines[0])
    sheep = set()
    dragon = (0, 0)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "S":
                sheep.add((x, y))
            elif c == "D":
                dragon = (x, y)

    sheep_count = 0
    stack = [(dragon, 0)]
    max_moves = 4
    while stack:
        pos, moves = stack.pop(0)
        if pos in sheep:
            sheep_count += 1
            sheep.remove(pos)
        if moves > max_moves - 1:
            continue
        x, y = pos
        for dx, dy in [
            (-2, 1),
            (-2, -1),
            (2, 1),
            (2, -1),
            (1, 2),
            (1, -2),
            (-1, 2),
            (-1, -2),
        ]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size_x and 0 <= ny < size_y:
                stack.append(((nx, ny), moves + 1))
    print(sheep_count)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
