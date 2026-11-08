import os, sys
import time
from enum import Enum
from collections import defaultdict


class Direction(Enum):
    UP = 0, -1
    DOWN = 0, 1
    LEFT = -1, 0
    RIGHT = 1, 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def turn90(self):
        if self == Direction.UP:
            return Direction.RIGHT
        if self == Direction.RIGHT:
            return Direction.DOWN
        if self == Direction.DOWN:
            return Direction.LEFT
        if self == Direction.LEFT:
            return Direction.UP
        return Direction.UP

    def turn180(self):
        if self == Direction.UP:
            return Direction.DOWN
        if self == Direction.RIGHT:
            return Direction.LEFT
        if self == Direction.DOWN:
            return Direction.UP
        if self == Direction.LEFT:
            return Direction.RIGHT
        return Direction.UP


class Ghost:
    def __init__(self, x: int, y: int, direction: Direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.collisions = 10000

    def move(
        self,
        walls: set[tuple[int, int]],
        width: int,
        height: int,
        per_coord_ghosts: dict[tuple[int, int], set["Ghost"]],
    ):
        nx, ny = self.x + self.direction.x, self.y + self.direction.y
        if nx < 0 or nx >= width or ny < 0 or ny >= height:
            self.direction = self.direction.turn90()
            self.collisions -= 1
            return self.collisions <= 0
        if (nx, ny) in walls:
            self.direction = self.direction.turn90()
            self.collisions -= 1
            return self.collisions <= 0
        per_coord_ghosts[(self.x, self.y)].remove(self)
        self.x = nx
        self.y = ny
        per_coord_ghosts[(self.x, self.y)].add(self)
        return self.collisions <= 0

    def check_ghost(self, per_coord_ghosts: dict[tuple[int, int], set["Ghost"]]):
        other_ghosts = per_coord_ghosts[(self.x, self.y)]
        if len(other_ghosts) > 1:
            self.direction = self.direction.turn180()
            self.collisions -= 1
            return self.collisions <= 0


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    walls: set[tuple[int, int]] = set()
    ghosts: set[Ghost] = set()
    per_coord_ghosts: dict[tuple[int, int], set[Ghost]] = defaultdict(set)
    width = len(lines[0])
    height = len(lines)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "#":
                walls.add((x, y))
                continue
            if c == ".":
                continue
            g = Ghost(0, 0, Direction.UP)
            if c == ">":
                g = Ghost(x, y, Direction.RIGHT)
            elif c == "<":
                g = Ghost(x, y, Direction.LEFT)
            elif c == "^":
                g = Ghost(x, y, Direction.UP)
            elif c == "v":
                g = Ghost(x, y, Direction.DOWN)
            ghosts.add(g)
            per_coord_ghosts[(x, y)].add(g)

    count = 0
    while len(ghosts) > 0:
        count += 1
        # print_grid(walls, per_coord_ghosts, width, height)
        to_be_removed: set[Ghost] = set()
        for ghost in ghosts:

            if ghost.move(walls, width, height, per_coord_ghosts):
                to_be_removed.add(ghost)
        ghosts -= to_be_removed
        for ghost in to_be_removed:
            per_coord_ghosts[(ghost.x, ghost.y)].remove(ghost)
        to_be_removed = set()
        for ghost in ghosts:
            if ghost.check_ghost(per_coord_ghosts):
                to_be_removed.add(ghost)
        ghosts -= to_be_removed
        for ghost in to_be_removed:
            per_coord_ghosts[(ghost.x, ghost.y)].remove(ghost)
    print(count)


def print_grid(
    walls: set[tuple[int, int]],
    per_coord_ghosts: dict[tuple[int, int], set[Ghost]],
    width: int,
    height: int,
):
    for y in range(height):
        row = ""
        for x in range(width):
            if (x, y) in walls:
                row += "#"
                continue
            ghosts = [*per_coord_ghosts[(x, y)]]
            if len(ghosts) > 1:
                row += str(len(ghosts))
            elif len(ghosts) == 1:
                if ghosts[0].direction == Direction.UP:
                    row += "^"
                elif ghosts[0].direction == Direction.RIGHT:
                    row += ">"
                elif ghosts[0].direction == Direction.DOWN:
                    row += "v"
                elif ghosts[0].direction == Direction.LEFT:
                    row += "<"
                else:
                    row += "?"
            else:
                row += "."
        print(row)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
