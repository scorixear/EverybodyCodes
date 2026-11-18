import os, sys
import time
from enum import Enum

sys.path.append(os.path.join(sys.path[0], "..", ".."))
from algorithms.dijkstra import Dijkstra

GREY = "\033[90m"
RESET = "\033[0m"

TOP = (0, -1)
LEFT = (-1, 0)
BOTTOM = (0, 1)
RIGHT = (1, 0)
CENTER = (0, 0)
DIRS = [TOP, LEFT, BOTTOM, RIGHT, CENTER]


class Corners(Enum):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_RIGHT = 2
    BOTTOM_LEFT = 3

    def opposite(self) -> "Corners":
        return Corners((self.value + 2) % 4)

    def neighbour(self, dir: tuple[int, int]) -> "list[Corners]":
        if dir == CENTER:
            return [Corners((self.value + 1) % 4), Corners((self.value + 3) % 4)]
        if dir == TOP:
            if self == Corners.BOTTOM_RIGHT or self == Corners.BOTTOM_LEFT:
                return []
            return (
                [Corners.BOTTOM_RIGHT]
                if self == Corners.TOP_RIGHT
                else [Corners.BOTTOM_LEFT]
            )
        if dir == RIGHT:
            if self == Corners.TOP_LEFT or self == Corners.BOTTOM_LEFT:
                return []
            return (
                [Corners.TOP_LEFT]
                if self == Corners.TOP_RIGHT
                else [Corners.BOTTOM_LEFT]
            )
        if dir == BOTTOM:
            if self == Corners.TOP_LEFT or self == Corners.TOP_RIGHT:
                return []
            return (
                [Corners.TOP_LEFT]
                if self == Corners.BOTTOM_LEFT
                else [Corners.TOP_RIGHT]
            )
        if self == Corners.TOP_RIGHT or self == Corners.BOTTOM_RIGHT:
            return []
        return (
            [Corners.TOP_RIGHT] if self == Corners.TOP_LEFT else [Corners.BOTTOM_RIGHT]
        )

    def border(self, other: "Corners"):
        match self:
            case Corners.TOP_LEFT:
                if other == Corners.TOP_RIGHT:
                    return (0, -1)
                if other == Corners.BOTTOM_LEFT:
                    return (-1, 0)
            case Corners.TOP_RIGHT:
                if other == Corners.BOTTOM_RIGHT:
                    return (1, 0)
                if other == Corners.TOP_LEFT:
                    return (0, -1)
            case Corners.BOTTOM_RIGHT:
                if other == Corners.BOTTOM_LEFT:
                    return (0, 1)
                if other == Corners.TOP_RIGHT:
                    return (1, 0)
            case Corners.BOTTOM_LEFT:
                if other == Corners.TOP_LEFT:
                    return (-1, 0)
                if other == Corners.BOTTOM_RIGHT:
                    return (0, 1)
        raise ValueError()

    def __lt__(self, other: "Corners"):
        return self.value < other.value


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    width = len(lines[0])
    height = len(lines)
    gaps = set(
        (x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == "."
    )
    start: tuple[int, int, Corners] = (0, 0, Corners.TOP_LEFT)
    end: tuple[int, int, Corners] = (width - 1, height - 1, Corners.BOTTOM_RIGHT)

    def neighbour(a: tuple[int, int, Corners]):
        x, y, corner = a
        result = []

        for d in DIRS:
            nx, ny = x + d[0], y + d[1]
            if not is_solid(nx, ny):
                continue
            for nc in corner.neighbour(d):
                if d == CENTER:
                    bx, by = corner.border(nc)
                    if is_solid(x + bx, y + by):
                        continue
                result.append((nx, ny, nc))
        return result

    def is_solid(x: int, y: int):
        return 0 <= x < width and 0 <= y < height and (x, y) not in gaps

    def cost(a, b):
        ax, ay, _ = a
        bx, by, _ = b
        if ax == bx and ay == by:
            return 1
        return 0

    alg = Dijkstra(neighbour, cost, 0)
    alg.find_path(start, end)
    print(alg.get_cost(end))

    def print_grid(grid: list[str], path: list[tuple[int, int, Corners]]):
        cells = {(x, y) for x, y, _ in path}
        for y, line in enumerate(grid):
            row = ""
            for x, c in enumerate(line):
                if (x, y) not in cells:
                    row += f"{GREY}{c}{RESET}"
                else:
                    row += c
            print(row)

    print_grid(lines, alg.get_path(end))


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
