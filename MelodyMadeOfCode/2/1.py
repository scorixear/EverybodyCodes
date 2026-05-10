import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    start = 0, 0
    bones = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "@":
                start = x, y
            elif c == "#":
                bones.add((x, y))
    moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    curr_move_i = 0
    curr_pos = start
    seen = set()
    while curr_pos not in bones:
        seen.add(curr_pos)
        next_pos = (
            curr_pos[0] + moves[curr_move_i][0],
            curr_pos[1] + moves[curr_move_i][1],
        )
        while next_pos in seen:
            curr_move_i = (curr_move_i + 1) % 4
            next_pos = (
                curr_pos[0] + moves[curr_move_i][0],
                curr_pos[1] + moves[curr_move_i][1],
            )
        curr_pos = next_pos
        curr_move_i = (curr_move_i + 1) % 4
        seen.add(curr_pos)
    print(len(seen) - 1)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
