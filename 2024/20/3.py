import os, sys
import time
import enum

class DIRECTION(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
class Type(enum.Enum):
    Wall = 0,
    Down = 1,
    Up = 2,
    Empty = 3
class Glider:
    def __init__(self, x: int, y: int, facing: DIRECTION, altitude: int):
        self.x = x
        self.y = y
        self.facing = facing
        self.altitude = altitude
    def clone(self):
        g = Glider(self.x, self.y, self.facing, self.altitude)
        return g
    def __repr__(self):
        return f"({self.x}, {self.y}, {self.facing} @ {self.altitude})"
    def __hash__(self):
        return hash((self.x, self.y, self.facing, self.altitude))
    def __eq__(self, other):
        if not isinstance(other, Glider):
            return False
        return (self.x, self.y, self.facing, self.altitude) == (other.x, other.y, other.facing, other.altitude)
    def can_move(self, grid: list[list[Type]]) -> bool:
        if self.facing == DIRECTION.UP:
            return self.y > 0 and grid[self.y-1][self.x] != Type.Wall
        elif self.facing == DIRECTION.RIGHT:
            return self.x < len(grid[0])-1 and grid[self.y][self.x+1] != Type.Wall
        elif self.facing == DIRECTION.DOWN:
            return self.y < len(grid)-1 and grid[self.y+1][self.x] != Type.Wall
        elif self.facing == DIRECTION.LEFT:
            return self.x > 0 and grid[self.y][self.x-1] != Type.Wall
        return True
    def move(self, grid: list[list[Type]]):
        if self.facing == DIRECTION.UP:
            self.y -= 1
        elif self.facing == DIRECTION.RIGHT:
            self.x += 1
        elif self.facing == DIRECTION.DOWN:
            self.y += 1
        elif self.facing == DIRECTION.LEFT:
            self.x -= 1
        if grid[self.y][self.x] == Type.Wall:
            raise Exception("Hit wall")
        elif grid[self.y][self.x] == Type.Up:
            self.altitude += 1
        elif grid[self.y][self.x] == Type.Down:
            self.altitude -= 2
        else:
            self.altitude -= 1
    def is_finished(self, grid: list[list[Type]]) -> bool:
        return self.y == len(grid)-1

    def turn_left(self):
        self.facing = DIRECTION((self.facing.value - 1) % 4)
    def turn_right(self):
        self.facing = DIRECTION((self.facing.value + 1) % 4)

def parse_grid(lines: list[str]) -> tuple[list[list[Type]], tuple[int,int]]:
    grid = []
    orig_start = (0,0)
    for y, line in enumerate(lines):
        row = []
        for x, char in enumerate(line):
            if char == ".":
                row.append(Type.Empty)
            elif char == "#":
                row.append(Type.Wall)
            elif char == "S":
                row.append(Type.Empty)
                orig_start = (x, y)
            elif char == "-":
                row.append(Type.Down)
            else:
                row.append(Type.Up)
        grid.append(row)
    row_count = len(grid)
    for _ in range(2):
        for row in range(row_count):
            grid.append(grid[row])
    return grid, orig_start
def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    grid, orig_start = parse_grid(lines)
    
            
    start_queue = [Glider(orig_start[0], 0, DIRECTION.DOWN, len(grid)+1)]
    visited_starts = set()
    altitude_loss: dict[int, tuple[int, int, int, bool]] = {x: (10000, 0, 0, False) for x in range(len(grid[0])) if grid[0][x] != Type.Wall}  # x: (best altitude loss, finished x, finished y)
    while start_queue:
        start = start_queue.pop()
        if start.x in visited_starts:
            continue
        visited_starts.add(start.x)
        bfs(start.x, start.y, start.altitude, grid, altitude_loss)
        next_start = altitude_loss[start.x]
        if not next_start[3]:
            continue
        new_glider = Glider(next_start[1], 0, DIRECTION.DOWN, start.altitude)
        start_queue.append(new_glider)
            
    curr_x = orig_start[0]
    curr_alt = 384400
    segment_counter = 0
    
    while curr_alt > 0:
        loss, fin_x, _, finished = altitude_loss[curr_x]
        if not finished:
            print("No more finished paths")
            break
        if curr_alt <= loss:
            break
        curr_alt -= loss
        curr_x = fin_x
        segment_counter += 1
    max_dist = bfs(curr_x, 0, curr_alt, grid, {x: (10000, 0, 0, False) for x in range(len(grid[0])) if grid[0][x] != Type.Wall})

    print(f"Distance: {segment_counter * len(grid) + max_dist}")
        
def bfs(start_x, start_y, start_alt: int, grid: list[list[Type]], alt_loss: dict[int, tuple[int, int, int, bool]]) -> int:
    visited = {}
    glider = Glider(start_x, start_y, DIRECTION.DOWN, start_alt)
    stack = [glider]
    max_dist = 0
    while stack:
        print(f"Stack size: {len(stack)}, visited states: {len(visited)}", end="\r")
        g = stack.pop()
        if g.altitude <= 0:
            if not alt_loss[start_x][3] and g.y > alt_loss[start_x][2]:
                max_dist = max(max_dist, g.y)
                alt_loss[start_x] = (alt_loss[start_x][0], g.x, g.y, False)
            continue
        if g in visited:
            continue
        visited[g] = g.altitude
        if g.is_finished(grid):
            loss = start_alt - g.altitude + 1
            if loss < alt_loss[start_x][0]:
                alt_loss[start_x] = (loss, g.x, g.y, True)
            continue
        if g.can_move(grid):
            gmove = g.clone()
            gmove.move(grid)
            stack.append(gmove)
        gturnl = g.clone()
        gturnl.turn_left()
        if gturnl.can_move(grid):
            gturnl.move(grid)
            stack.append(gturnl)
        gturnr = g.clone()
        gturnr.turn_right()
        if gturnr.can_move(grid):
            gturnr.move(grid)
            stack.append(gturnr)
    print()
    return max_dist

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
