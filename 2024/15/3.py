import os, sys
import time
from astar import AStar

def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
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
    middle = ['G', 'H', 'I', 'J', 'K']
    left = ['E', 'D', 'C', 'B', 'A']
    right = ['R', 'Q' ,'P', 'O', 'N']
    all = [left, middle, right]
    best = float('inf')
    for first in range(3):
        for second in range(3):
            if second == first:
                continue
            for third in range(3):
                if third == first or third == second:
                    continue
                for i in range(7):
                    acc_first = all[first]
                    acc_second = all[second]
                    acc_third = all[third]
                    if i & 1 == 1:
                        acc_first = acc_first[::-1]
                    if i & 2 == 2:
                        acc_second = acc_second[::-1]
                    if i & 4 == 4:
                        acc_third = acc_third[::-1]
                    route = acc_first + acc_second + acc_third
                    new_best =  collect_herbs(solver, cells, start, herbs, route)
                    if new_best < best:
                        best = new_best
                        print(f"New best: {best} with route {first}, {second}, {third} and inversion {i:03b}")
    print(F"Logical best: {collect_herbs(solver, cells, start, herbs, middle+left+right)}")              
    print(best)
def factorial(n: int) -> int:
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def collect_herbs(initial_solver: AStar[int, tuple[int,int]],
                  cells: set[tuple[int,int]],
                  start: tuple[int,int],
                  herbs:dict[str,set[tuple[int,int]]],
                  route: list[str]) -> int:
    if len(route) == 0:
        return_cost = initial_solver.get_cost(start)
        if return_cost is None:
            raise ValueError("No path to return to start")
        return return_cost
    min_cost = float('inf')
    next_herb = route[0]
    route = route[1:]
    min_herb_cost = float('inf')
    min_herb_pos = (0,0)
    herb_solver = create_solver(cells)
    herb_solver.find_path(start, None)
    for pos in herbs[next_herb]:
        cost = herb_solver.get_cost(pos)
        if cost is not None and cost < min_herb_cost:
            min_herb_cost = cost
            min_herb_pos = pos
    if min_herb_cost == float('inf'):
        raise ValueError(f"No path to herb {next_herb}")
    min_cost = min_herb_cost + collect_herbs(initial_solver, cells, min_herb_pos, herbs, route)
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
