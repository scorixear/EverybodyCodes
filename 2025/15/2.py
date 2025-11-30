import os, sys
import time
from enum import Enum
import dijkstra


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    maze = set()
    start = (0, 0)
    direction = Direction.NORTH
    curr = start
    instructions = lines[0].split(",")
    for ins in instructions:
        turn = ins[0]
        steps = int(ins[1:])
        if turn == "R":
            direction = Direction((direction.value + 1) % 4)
        else:
            direction = Direction((direction.value - 1) % 4)
        for _ in range(steps):
            new_pos_x = curr[0]
            new_pos_y = curr[1]
            if direction == Direction.NORTH:
                new_pos_y -= 1
            elif direction == Direction.EAST:
                new_pos_x += 1
            elif direction == Direction.SOUTH:
                new_pos_y += 1
            elif direction == Direction.WEST:
                new_pos_x -= 1
            curr = (new_pos_x, new_pos_y)
            maze.add(curr)
    end = curr
    maze.remove(end)
    min_x = min(pos[0] for pos in maze.union({start, end}))
    max_x = max(pos[0] for pos in maze.union({start, end}))
    min_y = min(pos[1] for pos in maze.union({start, end}))
    max_y = max(pos[1] for pos in maze.union({start, end}))
    print_maze(maze, start, end, min_x, max_x, min_y, max_y)

    algo = dijkstra.Dijkstra(
        lambda pos: find_neighbours(pos, maze, min_x, max_x, min_y, max_y),
        lambda a, b: 1,
        zero_cost=0,
    )
    algo.find_path(start, end)
    print("Result:", algo.get_cost(end))


def print_maze(maze, start, end, min_x, max_x, min_y, max_y):
    with open(os.path.join(sys.path[0], "output_maze.txt"), "w", encoding="utf-8") as f:
        for y in range(min_y, max_y + 1):
            line = ""
            for x in range(min_x, max_x + 1):
                pos = (x, y)
                if pos == start:
                    line += "S"
                elif pos == end:
                    line += "E"
                elif pos in maze:
                    line += "#"
                else:
                    line += " "
            f.write(line + "\n")


def find_neighbours(pos, maze, min_x, max_x, min_y, max_y):
    neighbours = []
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for delta in deltas:
        new_pos = (pos[0] + delta[0], pos[1] + delta[1])
        if (
            new_pos not in maze
            and min_x <= new_pos[0] <= max_x
            and min_y <= new_pos[1] <= max_y
        ):
            neighbours.append(new_pos)
    return neighbours


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
