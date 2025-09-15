import os, sys
import time
import enum

# Direction the gilder is facing
class DIRECTION(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
# Type of cell in the grid
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
    def tuple(self):
        return (self.x, self.y, self.facing, self.altitude)
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

    def turn_left(self):
        self.facing = DIRECTION((self.facing.value - 1) % 4)
    def turn_right(self):
        self.facing = DIRECTION((self.facing.value + 1) % 4)

def parse_grid() -> tuple[list[list[Type]], tuple[int,int]]:
    with open(os.path.join(sys.path[0],"i1.txt"), "r", encoding="utf-8") as f:
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
                row.append(Type.Empty)
                start = (x, y)
            elif char == "-":
                row.append(Type.Down)
            else:
                row.append(Type.Up)
        grid.append(row)
    return grid, start

def main():
    grid, start = parse_grid()

    # BFS Stack of (Glider, step)
    position_stack: list[tuple[Glider, int]] = []
    position_stack.append((Glider(start[0], start[1], DIRECTION.DOWN, 1000), 0))
    # Set of visited states (x, y, facing, altitude, step)
    visited = set()
    # Dynamic programming table of best altitude at each step
    dp = {}
    # while there are more positions to explore
    while position_stack:
        glider, step = position_stack.pop()
        # if the gilder is at the ground
        if glider.altitude <= 0:
            # and the step is not in dp
            if step not in dp:
                # set the best altitude to 0 and store the glider state
                dp[step] = (0, glider.clone())
            # if the step is in dp and the best altitude is less than 0
            elif dp[step][0] < 0:
                # update the best altitude to 0 and store the glider state
                dp[step] = (0, glider.clone())
            # no need to explore further from this state
            continue
        # if the step is 100, we are finished with this glider
        if step == 100:
            # update the dp
            if step not in dp:
                dp[step] = (glider.altitude, glider.clone())
            elif dp[step][0] < glider.altitude:
                dp[step] = (glider.altitude, glider.clone())
            continue
        # if we recorded an entry for this step
        if step in dp:
            # and the altitude reached is better than the recorded one
            if dp[step][0] < glider.altitude:
                # update the entry
                dp[step] = (glider.altitude, glider.clone())
        # record the state as visited
        state = glider.tuple() + (step,)
        if state in visited:
            continue
        visited.add(state)
        # explore the next states
        # move forward
        gmove = glider.clone()
        if gmove.can_move(grid):
            gmove.move(grid)
            position_stack.append((gmove, step+1))
        # move left
        gleft = glider.clone()
        gleft.turn_left()
        if gleft.can_move(grid):
            gleft.move(grid)
            position_stack.append((gleft, step+1))
        # move right
        gright = glider.clone()
        gright.turn_right()
        if gright.can_move(grid):
            gright.move(grid)
            position_stack.append((gright, step+1))
    # print the best altitude at step 100
    print(dp[100][0])
        

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
