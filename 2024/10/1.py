import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    grid = [list(line) for line in lines]
    final_word = []
    for row in range(2, 6):
        for col in range(2, 6):
            symbols_row = [grid[row][0], grid[row][1], grid[row][6], grid[row][7]]
            symbols_col = [grid[0][col], grid[1][col], grid[6][col], grid[7][col]]
            for symbol in symbols_row:
                if symbol in symbols_col:
                    final_word.append(symbol)
                    break
    print("".join(final_word))
            

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
