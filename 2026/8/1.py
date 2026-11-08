import os, sys
import time
from enum import Enum


class Direction(Enum):
    BOTTOM_RIGHT = (1,)
    BOTTOM_LEFT = (2,)
    RIGHT = (3,)
    LEFT = (4,)
    TOP_RIGHT = 5
    TOP_LEFT = 6

    def opposite(self):
        if self == Direction.BOTTOM_RIGHT:
            return Direction.TOP_LEFT
        if self == Direction.BOTTOM_LEFT:
            return Direction.TOP_RIGHT
        if self == Direction.RIGHT:
            return Direction.LEFT
        if self == Direction.LEFT:
            return Direction.RIGHT
        if self == Direction.TOP_RIGHT:
            return Direction.BOTTOM_LEFT
        if self == Direction.TOP_LEFT:
            return Direction.BOTTOM_RIGHT


class Ent:
    def __init__(self, height: int):
        self.height = height
        self.neighbours: dict[Direction, "Ent"] = {}
        self.blocked = False

    def is_start(self, direction: Direction):
        return direction.opposite() not in self.neighbours

    def set_neighbour(self, ent: "Ent", direction: Direction):
        self.neighbours[direction] = ent

    def block(self, direction: Direction, height: int):
        if height <= self.height:
            height = self.height
        else:
            self.blocked = True
            height -= 1
        if direction in self.neighbours:
            self.neighbours[direction].block(direction, height)


OFFSETS = {
    Direction.LEFT: (-2, 0),
    Direction.RIGHT: (2, 0),
    Direction.TOP_LEFT: (-1, -1),
    Direction.TOP_RIGHT: (1, -1),
    Direction.BOTTOM_LEFT: (-1, 1),
    Direction.BOTTOM_RIGHT: (1, 1),
}
YELLOW = "\033[93m"
GREY = "\033[90m"
RESET = "\033[0m"


def print_grid(ents):
    """Print the hex grid by rebuilding positions from the neighbour links only.
    Blocked ents are grey, the rest yellow."""
    os.system("")  # enables ANSI colours in the Windows console
    positions: dict[Ent, tuple[int, int]] = {}
    row_offset = 0
    for start in ents:
        if start in positions:
            continue
        # BFS over one connected component
        component = {start: (0, 0)}
        queue = [start]
        for ent in queue:
            x, y = component[ent]
            for direction, neighbour in ent.neighbours.items():
                if neighbour not in component:
                    dx, dy = OFFSETS[direction]
                    component[neighbour] = (x + dx, y + dy)
                    queue.append(neighbour)
        # normalise component so its top row starts below previous components
        min_y = min(y for _, y in component.values())
        for ent, (x, y) in component.items():
            positions[ent] = (x, y - min_y + row_offset)
        row_offset = max(y for _, y in positions.values()) + 2

    min_x = min(x for x, _ in positions.values())
    max_x = max(x for x, _ in positions.values())
    max_y = max(y for _, y in positions.values())
    cells = {pos: ent for ent, pos in positions.items()}
    for y in range(max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            ent = cells.get((x, y))
            if ent is None:
                row.append(" ")
            else:
                colour = GREY if ent.blocked else YELLOW
                row.append(f"{colour}{ent.height}{RESET}")
        print("".join(row).rstrip())


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    grid: dict[tuple[int, int], Ent] = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == ".":
                continue
            height = int(c)
            grid[(x, y)] = Ent(height)
    width = len(lines[0])
    height = len(lines)
    for (x, y), ent in grid.items():
        # top-left
        if y > 0 and x > 0 and (x - 1, y - 1) in grid:
            ent.set_neighbour(grid[(x - 1, y - 1)], Direction.TOP_LEFT)
        # top-right
        if y > 0 and x < width - 1 and (x + 1, y - 1) in grid:
            ent.set_neighbour(grid[(x + 1, y - 1)], Direction.TOP_RIGHT)
        # left
        if x > 1 and (x - 2, y) in grid:
            ent.set_neighbour(grid[(x - 2, y)], Direction.LEFT)
        # right
        if x < width - 2 and (x + 2, y) in grid:
            ent.set_neighbour(grid[(x + 2, y)], Direction.RIGHT)
        # bottom-left
        if x > 0 and y < height - 1 and (x - 1, y + 1) in grid:
            ent.set_neighbour(grid[(x - 1, y + 1)], Direction.BOTTOM_LEFT)
        # bottom-right
        if x < width - 1 and y < height - 1 and (x + 1, y + 1) in grid:
            ent.set_neighbour(grid[(x + 1, y + 1)], Direction.BOTTOM_RIGHT)
    for ent in grid.values():
        if ent.is_start(Direction.BOTTOM_RIGHT):
            ent.block(Direction.BOTTOM_RIGHT, 0)
    print_grid(grid.values())
    count = sum(1 for ent in grid.values() if not ent.blocked)
    print(count)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
