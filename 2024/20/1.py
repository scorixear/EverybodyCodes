import os, sys
import time
import enum

class DIRECTION(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    def __repr__(self) -> str:
        return "^" if self == DIRECTION.UP else ">" if self == DIRECTION.RIGHT else "v" if self == DIRECTION.DOWN else "<"
class Type(enum.Enum):
    Wall = 0,
    Down = 1,
    Up = 2,
    Empty = 3
class Glider:
    def __init__(self, x: int, y: int, facing: DIRECTION):
        self.x = x
        self.y = y
        self.facing = facing
        self.altitude = 1000
    def clone(self):
        g = Glider(self.x, self.y, self.facing)
        g.altitude = self.altitude
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

def main():
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

    position_stack: list[tuple[Glider, int]] = []
    position_stack.append((Glider(start[0], start[1], DIRECTION.DOWN), 0))
    visited = set()
    dp = {}
    while position_stack:
        glider, step = position_stack.pop()
        if glider.altitude <= 0:
            if step not in dp:
                dp[step] = (0, glider.clone())
            elif dp[step][0] < 0:
                dp[step] = (0, glider.clone())
            continue
        if step == 100:
            if step not in dp:
                dp[step] = (glider.altitude, glider.clone())
            elif dp[step][0] < glider.altitude:
                dp[step] = (glider.altitude, glider.clone())
            continue
        if step in dp:
            if dp[step][0] < glider.altitude:
                dp[step] = (glider.altitude, glider.clone())
            else:
                dp[step] = (dp[step][0], glider.clone())
        state = glider.tuple() + (step,)
        if state in visited:
            continue
        visited.add(state)
        if glider.can_move(grid):
            g = glider.clone()
            g.move(grid)
            position_stack.append((g, step+1))
        g = glider.clone()
        g.turn_left()
        if g.can_move(grid):
            g.move(grid)
            position_stack.append((g, step+1))
        g = glider.clone()
        g.turn_right()
        if g.can_move(grid):
            g.move(grid)
            position_stack.append((g, step+1))
    print(dp[100][0])
    print(dp[100][1])
        

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
