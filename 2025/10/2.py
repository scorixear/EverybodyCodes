import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    size_y = len(lines)
    size_x = len(lines[0])
    sheep = set()
    hideouts = set()
    dragon = (0, 0)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "S":
                sheep.add((x, y))
            elif c == "D":
                dragon = (x, y)
            elif c == "#":
                hideouts.add((x, y))

    sheep_count = 0
    max_moves = 20
    positions: dict[int, set[tuple[int, int]]] = {}
    current_positions = set([dragon])
    for move in range(max_moves + 1):
        next_positions = set()
        for pos in current_positions:
            x, y = pos
            positions.setdefault(move, set()).add(pos)

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
                    next_positions.add(((nx, ny)))
        current_positions = next_positions
    # print_grid(positions, size_x, size_y)
    for move, drag_pos in positions.items():
        for pos in drag_pos:
            if pos not in hideouts:
                sheep_pos = (pos[0], pos[1] - move)
                sheep_pre_move = (pos[0], pos[1] - move + 1)
                if sheep_pre_move in sheep:
                    sheep_count += 1
                    sheep.remove(sheep_pre_move)
                    # print(f"Sheep at {pos} caught in {move} moves")
                if sheep_pos in sheep:
                    sheep_count += 1
                    sheep.remove(sheep_pos)
                    # print(f"MOVED: Sheep at {sheep_pos} caught in {move} moves")

    print(sheep_count)


def print_grid(positions: dict[int, set[tuple[int, int]]], size_x: int, size_y: int):
    for move in positions.keys():
        for y in range(size_y):
            line = ""
            for x in range(size_x):
                if (x, y) in positions[move] and (x, y):
                    line += "X"
                else:
                    line += "."
            print(line)
        print()


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
