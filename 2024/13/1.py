import os, sys
import time
import astar

def main():
    with open(os.path.join(sys.path[0],"i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    grid = []
    start = (0,0)
    end = (0,0)
    for y, line in enumerate(lines):
        row = []
        for x, char in enumerate(line):
            if char == 'S':
                start = (x,y)
                row.append(0)
            elif char == 'E':
                end = (x,y)
                row.append(0)
            elif char == '#':
                row.append(-1)
            else:
                row.append(int(char))
        grid.append(row)
    solver = astar.AStar(lambda cell: get_neighbour(grid, cell), 
                         lambda cell1, cell2: get_cost(grid, cell1, cell2), 
                         lambda cell: heuristic(cell, end),
                         0)
    solver.find_path(start, end)
    print(solver.get_cost(end))
    pretty_print(grid, solver.get_path(end))

def get_neighbour(grid: list[list[int]], cell: tuple[int, int]) -> list[tuple[int, int]]:
    x, y = cell
    neighbours = []
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and grid[ny][nx] != -1:
            neighbours.append((nx, ny))
    return neighbours

def get_cost(grid: list[list[int]], cell1: tuple[int, int], cell2: tuple[int, int]) -> int:
    x1, y1 = cell1
    x2, y2 = cell2
    val1 = grid[y1][x1]
    val2 = grid[y2][x2]
    normal = abs(val2 - val1)
    overflow =  (val1 + 10 - val2 if val1 < val2 else 10 - val1 + val2)
    return min(normal, overflow) + 1

def heuristic(cell: tuple[int, int], end: tuple[int, int]) -> int:
    x1, y1 = cell
    x2, y2 = end
    return abs(x2 - x1) + abs(y2 - y1)

def pretty_print(grid: list[list[int]], path: list[tuple[int, int]]):
    path_set = set(path)
    for y, row in enumerate(grid):
        line = ""
        for x, val in enumerate(row):
            if (x,y) in path_set:
                line += f"\x1b[32m{val}\x1b[0m"
            elif val == -1:
                line += "\x1b[31m#\x1b[0m"
            else:
                line += str(val)
        print(line)

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
