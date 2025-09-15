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
    Empty = 3,
    Checkpoint_A = 4,
    Checkpoint_B = 5,
    Checkpoint_C = 6,
    Start = 7
class Glider:
    def __init__(self, x: int, y: int, facing: DIRECTION):
        self.x = x
        self.y = y
        self.facing = facing
        self.altitude = 10000
        self.checkpoints = 0
    def clone(self):
        g = Glider(self.x, self.y, self.facing)
        g.altitude = self.altitude
        g.checkpoints = self.checkpoints
        return g
    def __repr__(self):
        return f"({self.x}, {self.y}, {self.facing} @ {self.altitude} | {self.checkpoints})"
    def __hash__(self):
        return hash((self.x, self.y, self.facing, self.checkpoints))
    def can_move(self, grid: list[list[Type]]) -> bool:
        is_inside_grid = False
        grid_type = lambda _: Type.Wall
        
        if self.facing == DIRECTION.UP:
            is_inside_grid =  self.y > 0
            if not is_inside_grid:
                return False
            grid_type = lambda _: grid[self.y-1][self.x]
        elif self.facing == DIRECTION.RIGHT:
            is_inside_grid = self.x < len(grid[0])-1
            if not is_inside_grid:
                return False
            grid_type = lambda _: grid[self.y][self.x+1]
        elif self.facing == DIRECTION.DOWN:
            is_inside_grid = self.y < len(grid)-1
            if not is_inside_grid:
                return False
            grid_type = lambda _: grid[self.y+1][self.x]
        else:
            is_inside_grid = self.x > 0
            if not is_inside_grid:
                return False
            grid_type = lambda _: grid[self.y][self.x-1]
        gtype = grid_type(self)
        if gtype == Type.Wall:
            return False
        if gtype != Type.Start:
            return True
        if self.checkpoints < 3:
            return False
        if self.altitude < 10000:
            return False
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
        elif grid[self.y][self.x] == Type.Start:
            if self.checkpoints < 3:
                raise Exception("Hit start without all checkpoints")
            if self.altitude < 10000:
                raise Exception("Hit start without enough altitude")
            self.altitude -= 1
        else:
            self.altitude -= 1
            if grid[self.y][self.x] == Type.Checkpoint_A and self.checkpoints == 0:
                self.checkpoints += 1
            elif grid[self.y][self.x] == Type.Checkpoint_B and self.checkpoints == 1:
                self.checkpoints += 1
            elif grid[self.y][self.x] == Type.Checkpoint_C and self.checkpoints == 2:
                self.checkpoints += 1
    def is_finished(self, grid: list[list[Type]]) -> bool:
        return grid[self.y][self.x] == Type.Start and self.checkpoints == 3 and self.altitude >= 10000

    def turn_left(self):
        self.facing = DIRECTION((self.facing.value - 1) % 4)
    def turn_right(self):
        self.facing = DIRECTION((self.facing.value + 1) % 4)
        
def parse_grid() -> tuple[list[list[Type]], tuple[int,int]]:
    with open(os.path.join(sys.path[0],"i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    
    grid = []
    start = (0,0)
    for y, line in enumerate(lines):
        row = []
        for x, char in enumerate(line):
            if char == ".":
                row.append(Type.Empty)
            elif char == "#":
                row.append(Type.Wall)
            elif char == "S":
                row.append(Type.Start)
                start = (x, y)
            elif char == "-":
                row.append(Type.Down)
            elif char == "+":
                row.append(Type.Up)
            elif char == "A":
                row.append(Type.Checkpoint_A)
            elif char == "B":
                row.append(Type.Checkpoint_B)
            elif char == "C":
                row.append(Type.Checkpoint_C)
            else:
                raise Exception(f"Unknown char {char}")
        grid.append(row)
    return grid, start

def main():
    grid, start = parse_grid()

    # BFS Stack of [(Glider, step)]
    # Layered for each step iteration
    position_stack: list[list[tuple[Glider, int]]] = []
    position_stack.append([(Glider(start[0], start[1], DIRECTION.DOWN), 0)])
    # 4D list of best altitude at (x, y, checkpoints, facing)
    visited: list[list[list[list[int]]]] = [[[[-1 for _ in range(4)] for _ in range(4)] for _ in range(len(grid[0]))] for _ in range(len(grid))]
    # the finished gliders
    finished_gliders = []
    # total possible states just for tracking progress
    total_possible_states = len(grid)*len(grid[0])*4*4
    state_counter = 0
    loop_counter = 0
    # while we want to explore more positions
    while position_stack:
        loop_counter += 1
        print(f"Stack size: {len(position_stack)}, visited states: {len(visited)}/{total_possible_states}, finished gliders: {len(finished_gliders)}, loop_counter: {loop_counter}", end="\r")
        # Pop the current positions
        positions = position_stack.pop()
        next_positions = []
        # iterate over all positions in this step
        for glider, step in positions:
            state_counter += 1
            # get the recorded best altitude for this state
            visited_altitude = visited[glider.y][glider.x][glider.checkpoints][glider.facing.value]
            # if we have recorded a better altitude, skip this state
            if visited_altitude >= glider.altitude:
                continue
            # record the best altitude for this state
            visited[glider.y][glider.x][glider.checkpoints][glider.facing.value] = glider.altitude

            # if the glider is at the ground, skip it
            if glider.altitude <= 0:
                continue
            # explore the next states
            # move forward
            gmove = glider.clone()
            if gmove.can_move(grid):
                gmove.move(grid)
                if gmove.is_finished(grid):
                    finished_gliders.append((gmove, step+1))
                else:
                    next_positions.append((gmove, step+1))
            # turn left
            gturnl = glider.clone()
            gturnl.turn_left()
            if gturnl.can_move(grid):
                gturnl.move(grid)
                if gturnl.is_finished(grid):
                    finished_gliders.append((gturnl, step+1))
                else:
                    next_positions.append((gturnl, step+1))
            # turn right
            gturnr = glider.clone()
            gturnr.turn_right()
            if gturnr.can_move(grid):
                gturnr.move(grid)
                if gturnr.is_finished(grid):
                    finished_gliders.append((gturnr, step+1))
                else:
                    next_positions.append((gturnr, step+1))
        # if we found a finished glider, we can stop
        if finished_gliders:
            break
        # otherwise, if we have next positions, add them to the stack
        if next_positions:
            position_stack.append(next_positions)
    # sort the finished gliders by steps
    finished_gliders.sort(key=lambda x: x[1])
    print(f"Finished gliders: {len(finished_gliders)}")
    print(f"Best glider: {finished_gliders[0][1]} steps")

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
