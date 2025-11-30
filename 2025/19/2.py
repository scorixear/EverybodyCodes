import os, sys
import time


class Wall:
    def __init__(self, x, y, height):
        self.x = x
        self.passages = [(y, height)]

    def add_passage(self, y, height):
        self.passages.append((y, height))

    def is_in_passage(self, x, y):
        return self.x == x and any(y >= p[0] and y < p[0] + p[1] for p in self.passages)

    def is_in_wall(self, x, y):
        return self.x == x and not self.is_in_passage(x, y)


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    walls = {}
    for line in lines:
        parts = [int(x) for x in line.split(",")]
        if parts[0] not in walls:
            walls[parts[0]] = Wall(*parts)
        else:
            walls[parts[0]].add_passage(parts[1], parts[2])
    last_wall = walls[max(walls.keys())]

    start = (0, 0)
    queue: list[tuple[tuple[int, int], int]] = [(start, 0)]
    end_positions = {}
    visited = set()
    while queue:
        (x, y), flaps = queue.pop(0)
        if (x, y, flaps) in visited:
            continue
        visited.add((x, y, flaps))
        if last_wall.is_in_passage(x, y):
            if (x, y) not in end_positions or flaps < end_positions[(x, y)]:
                end_positions[(x, y)] = flaps
            continue
        next_x = x + 1
        new_pos1 = (next_x, y + 1)
        new_pos2 = (next_x, y - 1)
        if not any(wall.is_in_wall(*new_pos1) for wall in walls.values()):
            queue.append((new_pos1, flaps + 1))
        if new_pos2[1] >= 0 and not any(
            wall.is_in_wall(*new_pos2) for wall in walls.values()
        ):
            queue.append((new_pos2, flaps))
    print(min(end_positions.values()))


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
