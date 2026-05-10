import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    start = 0, 0
    bones = set()
    max_grid_x = 0
    max_grid_y = 0
    min_grid_x = 0
    min_grid_y = 0
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "@":
                start = x, y
            elif c == "#":
                bones.add((x, y))
            max_grid_x = max(max_grid_x, x)
        max_grid_y = max(max_grid_y, y)
    moves = [
        (0, -1),
        (0, -1),
        (0, -1),
        (1, 0),
        (1, 0),
        (1, 0),
        (0, 1),
        (0, 1),
        (0, 1),
        (-1, 0),
        (-1, 0),
        (-1, 0),
    ]

    curr_move_i = 0
    curr_pos = start
    seen = set(bones)
    for y in range(min_grid_y, max_grid_y + 1):
        for x in range(min_grid_x, max_grid_x + 1):
            if (x, y) in seen:
                continue
            if can_fill(seen, x, y, max_grid_x, max_grid_y, min_grid_x, min_grid_y):
                flood_fill(
                    seen,
                    x,
                    y,
                    max_grid_x,
                    max_grid_y,
                    min_grid_x,
                    min_grid_y,
                )
    step_count = 0
    while any(
        (bone[0] - 1, bone[1]) not in seen
        or (bone[0] + 1, bone[1]) not in seen
        or (bone[0], bone[1] - 1) not in seen
        or (bone[0], bone[1] + 1) not in seen
        for bone in bones
    ):
        seen.add(curr_pos)
        next_pos = (
            curr_pos[0] + moves[curr_move_i][0],
            curr_pos[1] + moves[curr_move_i][1],
        )
        while next_pos in seen:
            curr_move_i = (curr_move_i + 1) % len(moves)
            next_pos = (
                curr_pos[0] + moves[curr_move_i][0],
                curr_pos[1] + moves[curr_move_i][1],
            )
        curr_pos = next_pos
        max_grid_x = max(max_grid_x, curr_pos[0] + 2)
        max_grid_y = max(max_grid_y, curr_pos[1] + 2)
        min_grid_x = min(min_grid_x, curr_pos[0] - 2)
        min_grid_y = min(min_grid_y, curr_pos[1] - 2)
        curr_move_i = (curr_move_i + 1) % len(moves)
        seen.add(curr_pos)
        flood_fill(
            seen,
            curr_pos[0] + 1,
            curr_pos[1],
            max_grid_x,
            max_grid_y,
            min_grid_x,
            min_grid_y,
        )
        flood_fill(
            seen,
            curr_pos[0] - 1,
            curr_pos[1],
            max_grid_x,
            max_grid_y,
            min_grid_x,
            min_grid_y,
        )
        flood_fill(
            seen,
            curr_pos[0],
            curr_pos[1] + 1,
            max_grid_x,
            max_grid_y,
            min_grid_x,
            min_grid_y,
        )
        flood_fill(
            seen,
            curr_pos[0],
            curr_pos[1] - 1,
            max_grid_x,
            max_grid_y,
            min_grid_x,
            min_grid_y,
        )
        # print(f"Step {step_count}:")
        # print_grid(
        #     max_grid_x,
        #     max_grid_y,
        #     min_grid_x,
        #     min_grid_y,
        #     seen,
        #     bones,
        #     curr_pos,
        #     wait_for_input=False,
        # )
        step_count += 1
    print_grid(
        max_grid_x,
        max_grid_y,
        min_grid_x,
        min_grid_y,
        seen,
        bones,
        curr_pos,
        wait_for_input=False,
    )
    print(step_count)


def print_grid(
    max_grid_x: int,
    max_grid_y: int,
    min_grid_x: int,
    min_grid_y: int,
    seen: set[tuple[int, int]],
    bones: set[tuple[int, int]],
    curr_pos: tuple[int, int],
    wait_for_input: bool = True,
):
    for y in range(min_grid_y, max_grid_y + 1):
        for x in range(min_grid_x, max_grid_x + 1):
            if (x, y) in bones:
                print("#", end="")
            elif (x, y) == curr_pos:
                print("@", end="")
            elif (x, y) in seen:
                print("+", end="")
            else:
                print(".", end="")
        print()
    print()
    if wait_for_input:
        input("")


def flood_fill(
    seen: set[tuple[int, int]],
    x: int,
    y: int,
    max_grid_x: int,
    max_grid_y: int,
    min_grid_x: int,
    min_grid_y: int,
):
    if (x, y) in seen:
        return
    if can_fill(seen, x, y, max_grid_x, max_grid_y, min_grid_x, min_grid_y):
        stack = [(x, y)]
        while stack:
            curr = stack.pop()
            if curr in seen:
                continue
            seen.add(curr)
            stack.append((curr[0] + 1, curr[1]))
            stack.append((curr[0] - 1, curr[1]))
            stack.append((curr[0], curr[1] + 1))
            stack.append((curr[0], curr[1] - 1))


def can_fill(
    seen: set[tuple[int, int]],
    x: int,
    y: int,
    max_grid_x: int,
    max_grid_y: int,
    min_grid_x: int,
    min_grid_y: int,
) -> bool:
    new_seen = set(seen)
    stack = [(x, y)]
    curr = x, y
    while stack:
        curr = stack.pop()
        if curr in new_seen:
            continue
        if (
            curr[0] < min_grid_x
            or curr[1] < min_grid_y
            or curr[0] > max_grid_x
            or curr[1] > max_grid_y
        ):
            return False
        new_seen.add(curr)
        stack.append((curr[0] + 1, curr[1]))
        stack.append((curr[0] - 1, curr[1]))
        stack.append((curr[0], curr[1] + 1))
        stack.append((curr[0], curr[1] - 1))
    return True


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
