import os, sys
import time

class Cell:
    def __init__(self, x: int, y: int, height: int = 0):
        self.height: int = height
        self.x: int = x
        self.y: int = y
        self.neighbours = [[i, j] for i in range(x-1, x+2) for j in range(y-1, y+2) if (i, j) != (x, y)]
    def dig(self, cells: dict[tuple[int, int], "Cell"]):
        for x, y in self.neighbours:
            target_height = 0
            if (x, y) in cells:
                target_height = cells[(x,y)].height
            if target_height > self.height:
                return False, Cell(self.x, self.y, self.height)
        return True, Cell(self.x, self.y, self.height-1)
    def __str__(self):
        return f"Cell({self.x}, {self.y}, {self.height})"
    def __repr__(self):
        return str(self)
def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    cells: dict[tuple[int, int], Cell] = dict()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "#":
                cells[(x,y)] = Cell(x, y)
    has_digged = True
    counter = 0
    while has_digged:
        gen_counter, cells = generation(cells)
        if gen_counter == 0:
            has_digged = False
        counter += gen_counter
    print(counter)
    

def generation(cells: dict[tuple[int, int], Cell]):
    new_gen: dict[tuple[int, int], Cell] = dict()
    counter = 0
    for cell in cells.values():
        can_dig, new_cell = cell.dig(cells)
        if can_dig:
            counter += 1
        new_gen[(cell.x, cell.y)] = new_cell
    return counter, new_gen
if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
