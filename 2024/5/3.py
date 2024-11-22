import os, sys
import time

def main(before):
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    grid = [[int(x) for x in line.split()] for line in lines]
    grid = [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]
    current_row = 0
    max_round = 0
    counter = 1
    while True:
        result = calc_round(grid, current_row)
        if result > max_round:
            max_round = result
            print(f"Round {counter}: {result}")
            print(f"Time: {time.perf_counter() - before:.6f}s")
        current_row += 1
        if current_row >= len(grid):
            current_row = 0
        counter += 1
def calc_round(grid: list[list[int]], current_row: int):
    person = grid[current_row].pop(0)
    current_row = current_row + 1
    if current_row >= len(grid):
        current_row = 0
    row_len = len(grid[current_row])
    left_over = person % row_len
    current_mod = person // row_len
    if left_over == 0:
        left_over = row_len
        current_mod -= 1
    if current_mod % 2 == 0:
        grid[current_row].insert(left_over-1, person)
    else:
        grid[current_row].insert(row_len - left_over + 1, person)
    return int("".join([str(x[0]) for x in grid]))

if __name__ == "__main__":
    before = time.perf_counter()
    main(before)
    print(f"Time: {time.perf_counter() - before:.6f}s")
