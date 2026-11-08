import os, sys
import time
from enum import Enum
from collections import defaultdict

COLLISIONS = 1000000000000


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
        self.collisions = COLLISIONS

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
        return False

    def state(self):
        # everything that decides where this ghost goes next (collisions don't!)
        return (self.x, self.y, self.direction)


def remove_ghosts(
    ghosts: list[Ghost],
    to_be_removed: list[Ghost],
    per_coord_ghosts: dict[tuple[int, int], set[Ghost]],
):
    for ghost in to_be_removed:
        ghosts.remove(ghost)
        per_coord_ghosts[(ghost.x, ghost.y)].remove(ghost)


def step(
    ghosts: list[Ghost],
    walls: set[tuple[int, int]],
    width: int,
    height: int,
    per_coord_ghosts: dict[tuple[int, int], set[Ghost]],
) -> bool:
    """Simulates one tick. Returns True if at least one ghost vanished."""
    to_be_removed = [
        g for g in ghosts if g.move(walls, width, height, per_coord_ghosts)
    ]
    remove_ghosts(ghosts, to_be_removed, per_coord_ghosts)
    died = len(to_be_removed) > 0

    to_be_removed = [g for g in ghosts if g.check_ghost(per_coord_ghosts)]
    remove_ghosts(ghosts, to_be_removed, per_coord_ghosts)
    return died or len(to_be_removed) > 0


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    walls: set[tuple[int, int]] = set()
    # a list instead of a set, so the ghosts always have the same order
    # (needed to compare board states and to match collision counts up)
    ghosts: list[Ghost] = []
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
            ghosts.append(g)
            per_coord_ghosts[(x, y)].add(g)

    # Idea: the movement only depends on position + direction of every ghost.
    # The collision counter just decides when a ghost vanishes. So as long as
    # nobody vanishes, the board must eventually repeat -> a cycle. Once we
    # know the cycle, we can jump over many cycles at once.
    seen: dict[tuple, int] = {}  # board state -> tick it was first seen
    count = 0
    while len(ghosts) > 0:
        board = tuple(g.state() for g in ghosts)

        if board in seen:
            cycle_length = count - seen[board]

            # run the cycle once more and measure how many collisions each ghost uses
            collisions_before = [g.collisions for g in ghosts]
            died = False
            for _ in range(cycle_length):
                count += 1
                if step(ghosts, walls, width, height, per_coord_ghosts):
                    died = True
                    break

            if not died:
                used = [
                    before - g.collisions
                    for before, g in zip(collisions_before, ghosts)
                ]
                # how many cycles can we skip so that every ghost keeps at least 1 collision?
                skip = min(
                    (g.collisions - 1) // u for g, u in zip(ghosts, used) if u > 0
                )
                for g, u in zip(ghosts, used):
                    g.collisions -= skip * u
                count += skip * cycle_length

            # either a ghost vanished or we jumped ahead -> look for the next cycle
            seen.clear()
            continue

        seen[board] = count
        count += 1
        if step(ghosts, walls, width, height, per_coord_ghosts):
            # fewer ghosts -> different board, old states are useless now
            seen.clear()
    print(count)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
