import os, sys
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class Segment:
    x: int
    y: int
    width: int

    @property
    def end(self) -> int:
        return self.x + self.width - 1

    @staticmethod
    def parse(line: str) -> "Segment":
        x, y, w = [int(part.split("=")[1]) for part in line.split(" ")]
        return Segment(x, y, w)


class Coverage:
    """
    Row d spans from the smallest x to the largest end among all segments with y > d.
    That extent only changes at distinct y values, so sweep the segments from the
    highest y downwards and add each band of rows in one multiplication.
    """

    def __init__(self, segments: list[Segment]) -> None:
        self.segments: list[Segment] = sorted(segments, key=lambda s: s.y, reverse=True)

    def total(self) -> int:
        count: int = 0
        min_x: int = sys.maxsize
        max_end: int = -sys.maxsize
        for index, segment in enumerate(self.segments):
            min_x = min(min_x, segment.x)
            max_end = max(max_end, segment.end)
            band: int = segment.y - self.next_y(index)
            count += (max_end - min_x + 1) * band
        return count

    def next_y(self, index: int) -> int:
        if index + 1 < len(self.segments):
            return self.segments[index + 1].y
        return 0


def main() -> None:
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        lines: list[str] = f.read().strip().split("\n")
    segments: list[Segment] = [Segment.parse(line) for line in lines]
    print(Coverage(segments).total())


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
