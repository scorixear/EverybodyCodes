import os, sys
import time

GREEN = "\033[32m"
YELLOW = "\033[33m"
GREY = "\033[90m"
RESET = "\033[0m"


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    line = lines[0]
    sorted_idx = 0
    flip_count = 0
    while sorted_idx != len(line):
        sorted_idx, line, new_flip_count = flip(line, sorted_idx)
        flip_count += new_flip_count
    print(flip_count)


def flip(line: str, sorted_idx: int) -> tuple[int, str, int]:
    group = line[sorted_idx]
    sorted_idx += 1
    # find first group
    while sorted_idx < len(line):
        if line[sorted_idx] != group:
            break
        sorted_idx += 1
    if sorted_idx == len(line):
        return sorted_idx, line, 0
    # find last group
    back_idx = len(line) - 1
    in_group = False
    group_idx = len(line) - 1
    other_groups = []
    while back_idx >= sorted_idx:
        if line[back_idx] == group:
            if not in_group:
                in_group = True
                group_idx = back_idx
        else:
            if in_group:
                in_group = False
                other_groups.append((back_idx + 1, group_idx))
        back_idx -= 1
    if len(other_groups) == 0:
        return sorted_idx, line, 0
    # flip
    flip_count = 0
    while other_groups:
        print_state(line, sorted_idx, other_groups[0][0], other_groups)
        a, b = other_groups.pop(0)
        front = line[:sorted_idx]
        middle = line[sorted_idx : b + 1][::-1]
        back = line[b + 1 :]
        line = front + middle + back
        other_groups = [reverse_coords(x, y, sorted_idx, b) for x, y in other_groups][
            ::-1
        ]
        sorted_idx += b - a + 1
        flip_count += 1
    return sorted_idx, line, flip_count


def reverse_coords(a: int, b: int, start: int, end: int):
    new_b = end - (a - start)
    new_a = start + (end - b)
    return new_a, new_b


def print_state(line: str, sorted_idx: int, a: int, groups: list[tuple[int, int]]):
    output_line = f"{GREY}{line[:sorted_idx]}{RESET}"
    curr = sorted_idx
    for x, y in groups[::-1]:
        if curr < x:
            output_line += f"{line[curr:x]}"
            curr = y + 1
        if x == a:
            output_line += f"{GREEN}{line[x:y+1]}{RESET}"
        else:
            output_line += f"{YELLOW}{line[x:y+1]}{RESET}"
    output_line += f"{GREY}{line[curr:]}{RESET}"
    print(output_line)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
