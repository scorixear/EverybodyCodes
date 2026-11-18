import os
import re
import sys
import time
from dataclasses import dataclass


@dataclass
class Segment:
    start: int
    end: int
    reversed: bool

    def render(self, text: str) -> str:
        part = text[self.start : self.end]
        return part[::-1] if self.reversed else part


class FlipSorter:
    def __init__(self, line: str) -> None:
        self.unsorted = line
        self.flip_count = 0

    def solve(self) -> int:
        while self.unsorted:
            self.run_phase()
        return self.flip_count

    def run_phase(self) -> None:
        colour = self.unsorted[0]
        text = self.unsorted.lstrip(colour)
        runs = [m.span() for m in re.finditer(re.escape(colour) + "+", text)]
        if not runs:
            self.unsorted = text
            return
        tail = self.flip_runs(text, runs)
        self.unsorted = "".join(segment.render(text) for segment in tail)

    def flip_runs(self, text: str, runs: list[tuple[int, int]]) -> list[Segment]:
        left, right = 0, len(text)
        lo, hi = 0, len(runs) - 1
        forward = True
        tail: list[Segment] = []
        while lo <= hi:
            if forward:
                run_start, run_end = runs[hi]
                tail.append(Segment(run_end, right, False))
                self.flip_count += run_end - left
                right = run_start
                hi -= 1
            else:
                run_start, run_end = runs[lo]
                tail.append(Segment(left, run_start, True))
                self.flip_count += right - run_start
                left = run_end
                lo += 1
            forward = not forward
        tail.append(Segment(left, right, not forward))
        tail.reverse()
        return tail


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    line = lines[0] * 100
    print(FlipSorter(line).solve())


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
