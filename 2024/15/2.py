import os, sys
import time
from astar import AStar

def main():
    with open(os.path.join(sys.path[0],"i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    cells = set()
    herbs: dict[str, set[tuple[int,int]]] = {}
    start: tuple[int,int] = (0,0)
    for y, line in enumerate(lines):
        for x, cell in enumerate(line):
            if cell != "#":
                if cell == "." and y == 0:
                    start = (x,y)
                cells.add((x,y))
                if cell != ".":
                    herbs[cell] = herbs.get(cell, set())
                    herbs[cell].add((x,y))
    solver = create_solver(cells)
    solver.find_path(start, None)
    total = collect_herbs(solver, cells, start, herbs, set())
    print(total)

def collect_herbs(initial_solver: AStar[int, tuple[int,int]],
                  cells: set[tuple[int,int]],
                  start: tuple[int,int],
                  herbs:dict[str,set[tuple[int,int]]],
                  collected: set[str]) -> int:
    if len(collected) == len(herbs):
        return initial_solver.get_cost(start) or 0
    min_cost = float('inf')
    for herb, positions in herbs.items():
        if herb in collected:
            continue
        min_herb_cost = float('inf')
        min_herb_pos = (0,0)
        herb_solver = create_solver(cells)
        herb_solver.find_path(start, None)
        for pos in positions:
            cost = herb_solver.get_cost(pos)
            if cost is not None and cost < min_herb_cost:
                min_herb_cost = cost
                min_herb_pos = pos
        if min_herb_cost == float('inf'):
            continue
        new_collected = collected | {herb}
        min_cost = min(min_cost, min_herb_cost + collect_herbs(initial_solver, cells, min_herb_pos, herbs, new_collected))
    return int(min_cost)
    

def create_solver(cells: set[tuple[int,int]]) -> AStar[int, tuple[int,int]]:
    return AStar(
        lambda cell: [(cell[0]+dx, cell[1]+dy) for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)] if (cell[0]+dx, cell[1]+dy) in cells],
        lambda a,b: 1,
        lambda a: 1,
        0
    )    
if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
