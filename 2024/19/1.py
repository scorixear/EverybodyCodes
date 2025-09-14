import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    message = [c for c in lines[0]]
    
    grid = []
    for line in lines[2:]:
        row = []
        for c in line:
            row.append(c)
        grid.append(row)
    
    op_counter = 0
    for i in range(1, len(grid)-1):
        for j in range(1, len(grid[0])-1):
            op = message[op_counter % len(message)]
            if op == "R":
                rot_right(grid, j, i)
            elif op == "L":
                rot_left(grid, j, i)
            op_counter += 1
    print("\n".join("".join(row) for row in grid))
    
def rot_right(grid, x, y):
    a = grid[y-1][x-1]
    b = grid[y-1][x]
    c = grid[y-1][x+1]
    d = grid[y][x+1]
    e = grid[y+1][x+1]
    f = grid[y+1][x]
    g = grid[y+1][x-1]
    h = grid[y][x-1]
    
    grid[y-1][x-1] = h
    grid[y-1][x] = a
    grid[y-1][x+1] = b
    grid[y][x+1] = c
    grid[y+1][x+1] = d
    grid[y+1][x] = e
    grid[y+1][x-1] = f
    grid[y][x-1] = g

def rot_left(grid, x, y):
    a = grid[y-1][x-1]
    b = grid[y-1][x]
    c = grid[y-1][x+1]
    d = grid[y][x+1]
    e = grid[y+1][x+1]
    f = grid[y+1][x]
    g = grid[y+1][x-1]
    h = grid[y][x-1]
    
    grid[y-1][x-1] = b
    grid[y-1][x] = c
    grid[y-1][x+1] = d
    grid[y][x+1] = e
    grid[y+1][x+1] = f
    grid[y+1][x] = g
    grid[y+1][x-1] = h
    grid[y][x-1] = a
    

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
