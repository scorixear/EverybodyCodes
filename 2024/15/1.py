import os, sys
import time
from astar import AStar

def main():
    with open(os.path.join(sys.path[0],"i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    cells = set()
    herbs = []
    start: tuple[int,int] = (0,0)
    for y, line in enumerate(lines):
        for x, cell in enumerate(line):
            if cell != "#":
                if cell == "." and y == 0:
                    start = (x,y)
                cells.add((x,y))
                if cell == "H":
                    herbs.append((x,y))
    solver: AStar[int, tuple[int,int]] = AStar(
        lambda cell: [(cell[0]+dx, cell[1]+dy) for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)] if (cell[0]+dx, cell[1]+dy) in cells],
        lambda a,b: 1,
        lambda a: 1,
        0
    )
    solver.find_path(start, None)
    min_cost = float('inf')
    for herb in herbs:
        cost = solver.get_cost(herb)
        if cost is not None and cost < min_cost:
            min_cost = cost
    print(min_cost*2)
        
if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
