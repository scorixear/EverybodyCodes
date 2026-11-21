import os, sys
import time
from enum import Enum
from itertools import permutations


class Colour(Enum):
    CYAN = "C"
    MAGENTA = "M"
    YELLOW = "Y"
    BLACK = "K"
    BLUE = "B"
    GREEN = "G"
    RED = "R"

    def mix(self, other: "Colour"):
        if self == Colour.BLACK or other == Colour.BLACK:
            return Colour.BLACK
        if self.value == other.value:
            return Colour(self.value)
        match self:
            case Colour.CYAN:
                match other:
                    case Colour.MAGENTA:
                        return Colour.BLUE
                    case Colour.YELLOW:
                        return Colour.GREEN
            case Colour.MAGENTA:
                match other:
                    case Colour.CYAN:
                        return Colour.BLUE
                    case Colour.YELLOW:
                        return Colour.RED
            case Colour.YELLOW:
                match other:
                    case Colour.CYAN:
                        return Colour.GREEN
                    case Colour.MAGENTA:
                        return Colour.RED
        raise ValueError()


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    grid1: dict[tuple[int, int], Colour] = {}
    grid2: dict[tuple[int, int], int] = {}
    is_grid2 = False
    y = 0
    for line in lines:
        if is_grid2:
            for x, c in enumerate(line):
                grid2[(x, y)] = int(c)
        elif len(line.strip()) == 0:
            is_grid2 = True
            y = 0
            continue
        else:
            for x, c in enumerate(line):
                grid1[(x, y)] = Colour(c)
        y += 1

    perms = permutations([1, 2, 3, 4])
    total = 0
    for y, m, c, k in perms:
        total = max(
            total,
            calc_total(
                grid1,
                grid2,
                {y: Colour.YELLOW, m: Colour.MAGENTA, c: Colour.CYAN, k: Colour.BLACK},
            ),
        )

    print(total)


def calc_total(
    grid1: dict[tuple[int, int], Colour],
    grid2: dict[tuple[int, int], int],
    lookup: dict[int, Colour],
):
    counts: dict[Colour, int] = {}
    for key, colour in grid1.items():
        other = lookup[grid2[key]]
        mixed = colour.mix(other)
        if mixed not in counts:
            counts[mixed] = 1
        else:
            counts[mixed] = counts[mixed] + 1
    total = 1
    for c in sorted(counts.values(), reverse=True)[:3]:
        total *= c
    return total


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
