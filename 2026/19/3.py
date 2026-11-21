import os, sys
import time
from enum import Enum
from itertools import combinations

from PIL import Image


class Colour(Enum):
    CYAN = "C"
    MAGENTA = "M"
    YELLOW = "Y"
    BLACK = "K"
    BLUE = "B"
    GREEN = "G"
    RED = "R"

    @staticmethod
    def primaries() -> list["Colour"]:
        return [Colour.YELLOW, Colour.MAGENTA, Colour.CYAN]

    def mix(self, other: "Colour") -> "Colour":
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

    def rgb(self) -> tuple[int, int, int]:
        match self:
            case Colour.CYAN:
                return (0, 255, 255)
            case Colour.MAGENTA:
                return (255, 0, 255)
            case Colour.YELLOW:
                return (255, 255, 0)
            case Colour.BLACK:
                return (0, 0, 0)
            case Colour.BLUE:
                return (0, 0, 255)
            case Colour.GREEN:
                return (0, 255, 0)
            case Colour.RED:
                return (255, 0, 0)

    def reachable(self) -> set["Colour"]:
        return {self.mix(p) for p in Colour.primaries()}


class Picture:
    """Saves a colour grid as an image: one cell = one pixel."""

    def __init__(self, grid: list[list[Colour]]) -> None:
        self.grid: list[list[Colour]] = grid

    def save(self, path: str) -> None:
        height: int = len(self.grid)
        width: int = max(len(row) for row in self.grid)
        image: Image.Image = Image.new("RGB", (width, height))
        for y, row in enumerate(self.grid):
            for x, colour in enumerate(row):
                image.putpixel((x, y), colour.rgb())
        image.save(path)


Targets = tuple[Colour, Colour, Colour]
Amounts = tuple[int, int, int]


class Part3:
    def __init__(self, grid: list[list[Colour]]) -> None:
        self.grid: list[list[Colour]] = grid
        self.counts: dict[Colour, int] = {}
        for row in grid:
            for colour in row:
                self.counts[colour] = self.counts.get(colour, 0) + 1
        self.reach: dict[Colour, set[Colour]] = {src: src.reachable() for src in self.counts}

    @staticmethod
    def load(path: str) -> list[list[Colour]]:
        with open(path, "r", encoding="utf-8") as f:
            lines: list[str] = f.read().strip().split("\n")
        return [[Colour(c) for c in line.strip()] for line in lines if line.strip()]

    # ---------- scoring ----------

    def score(self, chosen: list[list[Colour]]) -> int:
        counts: dict[Colour, int] = {}
        for row, chosen_row in zip(self.grid, chosen):
            for colour, other in zip(row, chosen_row):
                mixed: Colour = colour.mix(other)
                counts[mixed] = counts.get(mixed, 0) + 1
        total: int = 1
        for c in sorted(counts.values(), reverse=True)[:3]:
            total *= c
        return total

    # ---------- optimisation ----------

    def supply(self, targets: set[Colour]) -> int:
        """How many cells can be turned into at least one colour of `targets`."""
        return sum(n for src, n in self.counts.items() if self.reach[src] & targets)

    def best_for(self, targets: Targets) -> tuple[int, Amounts]:
        """Max product of the three target counts. The feasible counts form a
        polymatroid: x(A) <= supply(A) for every subset A of the targets."""
        s1, s2, s3 = targets
        f1: int = self.supply({s1})
        f2: int = self.supply({s2})
        f3: int = self.supply({s3})
        f12: int = self.supply({s1, s2})
        f13: int = self.supply({s1, s3})
        f23: int = self.supply({s2, s3})
        f123: int = self.supply({s1, s2, s3})
        best: tuple[int, Amounts] = (-1, (0, 0, 0))
        for x1 in range(f1 + 1):
            cap2: int = min(f2, f12 - x1)
            cap3: int = min(f3, f13 - x1)
            pair: int = min(f23, f123 - x1, cap2 + cap3)
            for x2 in self.splits(pair, cap2, cap3):
                amounts: Amounts = (x1, x2, pair - x2)
                if self.product(amounts) > best[0]:
                    best = (self.product(amounts), amounts)
        return best

    @staticmethod
    def splits(pair: int, cap2: int, cap3: int) -> list[int]:
        """Candidate x2 values: as balanced as possible, or everything on one side
        (an absent colour is skipped by the top-3 product, so tiny grids prefer that)."""
        balanced: int = max(pair - cap3, min(cap2, pair // 2))
        lopsided: int = cap2 if cap2 >= pair else pair - cap3
        return [balanced, lopsided]

    @staticmethod
    def product(amounts: Amounts) -> int:
        """Top-3 product as the puzzle scores it: colours with count 0 don't exist."""
        present: list[int] = [a for a in amounts if a > 0]
        total: int = 1
        for a in present:
            total *= a
        return total if present else 0

    def best_targets(self) -> tuple[Targets, Amounts]:
        best_product: int = -1
        best: tuple[Targets, Amounts] = ((Colour.CYAN, Colour.CYAN, Colour.CYAN), (0, 0, 0))
        for targets in combinations(list(Colour), 3):
            product, amounts = self.best_for(targets)
            if product > best_product:
                best_product = product
                best = (targets, amounts)
        return best

    # ---------- building the grid ----------

    def achievable(self, needed: dict[Colour, int], left: dict[Colour, int]) -> bool:
        """Can the cells not yet filled in (`left`) still deliver `needed`?
        True iff every group of targets has enough cells able to reach it."""
        for size in range(1, len(needed) + 1):
            for group in combinations(needed, size):
                need: int = sum(needed[target] for target in group)
                have: int = sum(n for src, n in left.items() if self.reach[src] & set(group))
                if need > have:
                    return False
        return True

    def choose(self, colour: Colour, needed: dict[Colour, int], left: dict[Colour, int]) -> Colour:
        """Use this cell for a target colour, as long as the rest stays achievable."""
        left[colour] -= 1
        for primary in Colour.primaries():
            target: Colour = colour.mix(primary)
            if needed.get(target, 0) > 0:
                needed[target] -= 1
                if self.achievable(needed, left):
                    return primary
                needed[target] += 1
        return Colour.YELLOW  # cell is not needed for the top 3

    def build(self, targets: Targets, amounts: Amounts) -> list[list[Colour]]:
        needed: dict[Colour, int] = dict(zip(targets, amounts))
        left: dict[Colour, int] = dict(self.counts)
        return [[self.choose(colour, needed, left) for colour in row] for row in self.grid]

    def solve(self) -> tuple[int, list[list[Colour]]]:
        targets, amounts = self.best_targets()
        chosen: list[list[Colour]] = self.build(targets, amounts)
        return self.score(chosen), chosen

    @staticmethod
    def main() -> None:
        grid: list[list[Colour]] = Part3.load(os.path.join(sys.path[0], "i3.txt"))
        result, chosen = Part3(grid).solve()
        print(result)
        mixed: list[list[Colour]] = [
            [colour.mix(other) for colour, other in zip(row, chosen_row)]
            for row, chosen_row in zip(grid, chosen)
        ]
        Picture(grid).save(os.path.join(sys.path[0], "input.png"))
        Picture(chosen).save(os.path.join(sys.path[0], "chosen.png"))
        Picture(mixed).save(os.path.join(sys.path[0], "mixed.png"))


if __name__ == "__main__":
    before = time.perf_counter()
    Part3.main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
