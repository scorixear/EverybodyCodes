import os, sys
import time
import heapq

# How the plant grows (see 2.py for the full simulation):
#
# * Every branch is a counter that grows by 1 each second.
# * When a branch would reach `growth`, it splits instead:
#     - the branch shrinks to half size
#     - a new "left" branch of half size is created (it takes over the children)
#     - a new "right" twig of size 1 is created
# * Each split adds exactly ONE leaf to the plant.
#
# So we never need the tree itself. We only need to know WHEN splits happen:
#
#   * a fresh twig (size 1) splits after  growth - 1          seconds
#   * a half-size branch splits after     growth - half_size  seconds
#
# Every split produces 1 fresh twig and 2 half-size branches (the shrunk
# branch itself and the new left branch). Each of them will split again later.
#
# We keep a calendar: "at second X, N branches will split". We always jump to
# the next date in the calendar, count its splits as new leaves, and schedule
# the follow-up splits. This skips all the seconds where nothing happens.


class SplitCalendar:
    """Remembers how many branches split at which second."""

    def __init__(self):
        self.splits_at: dict[int, int] = {}  # second -> number of splits
        self.upcoming_seconds: list[int] = []  # min-heap of scheduled seconds

    def schedule(self, second: int, number_of_splits: int):
        if second not in self.splits_at:
            self.splits_at[second] = 0
            heapq.heappush(self.upcoming_seconds, second)
        self.splits_at[second] += number_of_splits

    def next_event(self) -> tuple[int, int]:
        """Remove and return (second, number_of_splits) of the earliest event."""
        second = heapq.heappop(self.upcoming_seconds)
        return second, self.splits_at.pop(second)


def split_delays(growth: int) -> tuple[int, int]:
    """Seconds until a fresh twig / a half-size branch reaches its split."""
    half_size = (growth - 1) // 2
    twig_delay = growth - 1  # a twig starts at size 1
    half_branch_delay = growth - half_size
    return twig_delay, half_branch_delay


def seconds_until_limit(growth: int, limit: int) -> int:
    """Number of seconds until the plant has at least `limit` leaves."""
    if limit <= 0:
        return 0

    twig_delay, half_branch_delay = split_delays(growth)

    # second 1: the seed sprouts into a single twig (= 1 leaf)
    second = 1
    leaves = 1
    calendar = SplitCalendar()
    calendar.schedule(second + twig_delay, 1)

    while leaves < limit:
        second, splits = calendar.next_event()
        leaves += splits  # every split adds one leaf

        # each split creates 1 fresh twig and 2 half-size branches
        calendar.schedule(second + twig_delay, splits)
        calendar.schedule(second + half_branch_delay, 2 * splits)

    return second


def parse_line(line: str) -> tuple[int, int]:
    """'id=1, growth=3, limit=10' -> (3, 10)"""
    _, growth, limit = line.split(", ")
    return int(growth.split("=")[1]), int(limit.split("=")[1])


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        lines = f.read().strip().split("\n")

    total = 0
    for line in lines:
        growth, limit = parse_line(line)
        total += seconds_until_limit(growth, limit)
    print(total)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
