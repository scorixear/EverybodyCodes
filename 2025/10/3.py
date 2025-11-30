import os, sys
import time

directions = [
    (-2, 1),
    (-2, -1),
    (2, 1),
    (2, -1),
    (1, 2),
    (1, -2),
    (-1, 2),
    (-1, -2),
]


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
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

    dp = {}
    done = calculate(dragon, size_x, size_y, hideouts, sheep, True, dp)
    print(done)


def calculate(pos, size_x, size_y, hideouts, sheep, sheep_turn, dp):
    # Base case: all sheep caught - we found a solution
    if len(sheep) == 0:
        return 1
    key = (pos, frozenset(sheep), sheep_turn)
    if key in dp:
        return dp[key]
    total = 0
    if sheep_turn:
        found_move = False
        for sx, sy in sheep:
            # prioritize moving of the board
            if sy + 1 == size_y:
                found_move = True
            # prioritize hideout or non-dragon position
            elif (sx, sy + 1) in hideouts or (sx, sy + 1) != pos:
                new_sheep = sheep.copy()
                new_sheep.remove((sx, sy))
                new_sheep.add((sx, sy + 1))
                total += calculate(pos, size_x, size_y, hideouts, new_sheep, False, dp)
                found_move = True
        # no valid moves found, so sheep do not move
        if not found_move:
            total += calculate(pos, size_x, size_y, hideouts, sheep, False, dp)
    else:
        for dx, dy in directions:
            nx, ny = pos[0] + dx, pos[1] + dy
            if 0 <= nx < size_x and 0 <= ny < size_y:
                new_sheep = sheep
                # we ate a sheep at new position
                if (nx, ny) not in hideouts:
                    new_sheep = new_sheep - {(nx, ny)}
                total += calculate(
                    (nx, ny), size_x, size_y, hideouts, new_sheep, True, dp
                )
    dp[key] = total
    return total


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
