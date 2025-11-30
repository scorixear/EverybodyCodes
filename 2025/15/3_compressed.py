import os, sys
import time
from collections import defaultdict
from heapq import heappop, heappush
import random


def build_wall(instr):
    x, y, dx, dy = 0, 0, 0, 1
    wall = {(x, y)}
    for direct, amount in instr:
        dx, dy = (-dy, dx) if direct == "L" else (dy, -dx)
        for _ in range(amount):
            x += dx
            y += dy
            wall.add((x, y))
    return (0, 0), (x, y), wall


class CoordinateCompression:
    def __init__(self, original_values: set[int], n_bits: int = 64):
        self._rand_bits = random.getrandbits(n_bits)
        self._orig_vals: list[int] = []
        self._map: dict[int, int] = {}
        for x in sorted(original_values):
            if not self._orig_vals or x != self._orig_vals[-1]:
                self._orig_vals += [x]
                self._map[x ^ self._rand_bits] = len(self._map)
        self.n = len(self._orig_vals)

    def compressed_value(self, original_value: int) -> int:
        return self._map[original_value ^ self._rand_bits]

    def original_value(self, compressed_value: int) -> int:
        return self._orig_vals[compressed_value]

    def n_compressed_values(self) -> int:
        return self.n


def build_wall_segments(
    instr: list[tuple[str, int]],
) -> tuple[tuple[int, int], tuple[int, int], list[tuple[int, int, int, int]]]:
    x: int = 0
    y: int = 0
    dx: int = 0
    dy: int = 1
    wall_segments: list[tuple[int, int, int, int]] = []
    for direct, amount in instr:
        dx, dy = (-dy, dx) if direct == "L" else (dy, -dx)
        new_x, new_y = x + amount * dx, y + amount * dy
        wall_segments.append((x, y, new_x, new_y))
        x, y = new_x, new_y
    return (0, 0), (x, y), wall_segments


def init_compression(
    wall_segments: list[tuple[int, int, int, int]],
) -> tuple[CoordinateCompression, CoordinateCompression]:
    x_values: set[int] = set()
    y_values: set[int] = set()
    for x1, y1, x2, y2 in wall_segments:
        x_values.update([x1 - 1, x1, x1 + 1, x2 - 1, x2, x2 + 1])
        y_values.update([y1 - 1, y1, y1 + 1, y2 - 1, y2, y2 + 1])
    return CoordinateCompression(x_values), CoordinateCompression(y_values)


def compress(
    start: tuple[int, int],
    end: tuple[int, int],
    wall_segments: list[tuple[int, int, int, int]],
    compression: tuple[CoordinateCompression, CoordinateCompression],
) -> tuple[tuple[int, int], tuple[int, int], set[tuple[int, int]]]:
    compressed_start: tuple[int, int] = (
        compression[0].compressed_value(start[0]),
        compression[1].compressed_value(start[1]),
    )
    compressed_end: tuple[int, int] = (
        compression[0].compressed_value(end[0]),
        compression[1].compressed_value(end[1]),
    )
    wall = set()
    for x1, y1, x2, y2 in wall_segments:
        x1 = compression[0].compressed_value(x1)
        y1 = compression[1].compressed_value(y1)
        x2 = compression[0].compressed_value(x2)
        y2 = compression[1].compressed_value(y2)
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                wall.add((x1, y))
        else:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                wall.add((x, y1))
    return compressed_start, compressed_end, wall


def calc_dist(
    start: tuple[int, int],
    end: tuple[int, int],
    wall: set[tuple[int, int]],
    compression: tuple[CoordinateCompression, CoordinateCompression],
) -> int:
    x_min: int = 0
    x_max: int = compression[0].n_compressed_values() - 1
    y_min: int = 0
    y_max: int = compression[1].n_compressed_values() - 1
    dist: defaultdict[tuple[int, int], int] = defaultdict(lambda: 1 << 63)
    dist[start] = 0
    queue = [(0, start)]
    while queue:
        distance, (x, y) = heappop(queue)
        if distance != dist[x, y]:
            continue
        if (x, y) == end:
            return distance
        for xn, yn in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if xn < x_min or xn > x_max or yn < y_min or yn > y_max:
                continue
            dx = abs(
                compression[0].original_value(x) - compression[0].original_value(xn)
            )
            dy = abs(
                compression[1].original_value(y) - compression[1].original_value(yn)
            )
            dn = distance + dx + dy
            if (xn, yn) == end or (xn, yn) not in wall:
                if dn < dist[xn, yn]:
                    dist[xn, yn] = dn
                    heappush(queue, (dn, (xn, yn)))
    assert False


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    instr: list[tuple[str, int]] = [(x[0], int(x[1:])) for x in lines[0].split(",")]

    start, end, wall_segments = build_wall_segments(instr)
    compression = init_compression(wall_segments)
    start, end, wall = compress(start, end, wall_segments, compression)
    ans3 = calc_dist(start, end, wall, compression)
    print("Result:", ans3)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
