import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    active_cells = set()
    base_width = 13
    base_height = 13
    width = base_width * 2 + len(lines[0])
    height = base_height * 2 + len(lines)
    pattern_cells = set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                pattern_cells.add((base_width + x, base_height + y, True))
            else:
                pattern_cells.add((base_width + x, base_height + y, False))
    seen = set()
    match_at = {}
    counted_cells = 0
    simulated_rounds = 0
    for round in range(1_000_000_000):
        print(f"Round: {round}", end="\r")
        new_active_cells = set()
        for y in range(0, height):
            for x in range(0, width):
                neighbours = 0
                for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                    nx, ny = x + dx, y + dy
                    if (
                        0 <= nx < width
                        and 0 <= ny < height
                        and (nx, ny) in active_cells
                    ):
                        neighbours += 1
                if (x, y) in active_cells:
                    if neighbours % 2 == 1:
                        new_active_cells.add((x, y))
                elif neighbours % 2 == 0:
                    new_active_cells.add((x, y))

        all_matched = True
        for cell in pattern_cells:
            if cell[2] and (cell[0], cell[1]) not in new_active_cells:
                all_matched = False
                break
            if not cell[2] and (cell[0], cell[1]) in new_active_cells:
                all_matched = False
                break
        # print_grid(new_active_cells, width, height)
        if all_matched:
            print_grid(new_active_cells, width, height)
            print(f"Matched at round {round}")
            print(f"Active cells: {len(new_active_cells)}")
            match_at[round] = len(new_active_cells)
            counted_cells += len(new_active_cells)
        if tuple(new_active_cells) in seen:
            # print_grid(new_active_cells, width, height)
            active_cells = new_active_cells
            simulated_rounds = round
            break
        seen.add(tuple(new_active_cells))
        active_cells = new_active_cells

    print(f"Counted cells: {counted_cells}")
    cycle_length = simulated_rounds
    print(f"Cycle length: {cycle_length}")
    left_over = 1_000_000_000 % simulated_rounds
    cycle_count = 1_000_000_000 // simulated_rounds
    print(f"Cycle count: {cycle_count}, left over: {left_over}")
    total = counted_cells * cycle_count
    for r in range(left_over):
        if r in match_at:
            total += match_at[r]

    print(total)


def print_grid(cells, width, height):
    print()
    for y in range(height):
        line = ""
        for x in range(width):
            if (x, y) in cells:
                line += "#"
            else:
                line += "."
        print(line)
    print()


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
