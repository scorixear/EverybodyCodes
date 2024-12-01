import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    grids = []
    for i in range(0, len(lines), 9):
        for j in range(0, len(lines[i]), 9):
            grids.append([list(line[j:j+8]) for line in lines[i:i+8]])

    total = 0
    for grid in grids:
        word = find_word(grid)
        base_power = [ord(symbol) - 64 for symbol in word]
        powers = [p * i for i, p in enumerate(base_power, 1)]
        total += sum(powers)
    
    print(total)

def find_word(grid: list[list[str]]) -> list[str]:
    final_word = []
    for row in range(2, 6):
        for col in range(2, 6):
            symbols_row = [grid[row][0], grid[row][1], grid[row][6], grid[row][7]]
            symbols_col = [grid[0][col], grid[1][col], grid[6][col], grid[7][col]]
            for symbol in symbols_row:
                if symbol in symbols_col:
                    final_word.append(symbol)
                    break
    return final_word

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
