import os, sys
import time
import hashlib

def grid_hash(grid):
    return hashlib.sha256("".join("".join(row) for row in grid).encode()).hexdigest()

def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    message = list(lines[0])
    
    grid = []
    for line in lines[2:]:
        row = []
        for c in line:
            row.append(c)
        grid.append(row)
    counter = 0
    seen_grids = {grid_hash(grid): 0}
    do_not_calculate = False
    while counter < 1048576000:
        print(f"Round {counter+1}/1048576000")
        counter += 1
        op_counter = 0
        for i in range(1, len(grid)-1):
            for j in range(1, len(grid[0])-1):
                op = message[op_counter % len(message)]
                if op == "R":
                    rot_right(grid, j, i)
                elif op == "L":
                    rot_left(grid, j, i)
                op_counter += 1
        if do_not_calculate:
            continue
        h = grid_hash(grid)
        if h in seen_grids:
            index = seen_grids[h]
            print(f"Cycle detected! Length: {counter - index - 1}")
            cycle_length = counter - index - 1
            remaining = (1048576000 - counter) % cycle_length
            counter = 1048576000 - remaining
            do_not_calculate = True
        else:
            seen_grids[h] = counter
            
    print("\n".join("".join(row) for row in grid))
def copy_grid(grid):
    new_grid = []
    for i in range(len(grid)):
        new_grid.append(grid[i].copy())
    return new_grid
def is_identical_grid(seen_grids, grid):
    for count, g in enumerate(seen_grids):
        identical = True
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if g[i][j] != grid[i][j]:
                    identical = False
                    break
            if not identical:
                break
        if identical:
            return True, count
    return False, 0
  
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
