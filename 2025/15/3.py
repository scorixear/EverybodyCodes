import os, sys
import time
from enum import Enum
import dijkstra
import astar


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    maze = []
    start = (0, 0)
    end = (0, 0)
    direction = Direction.NORTH
    curr = start
    instructions = lines[0].split(",")
    for i, ins in enumerate(instructions):
        turn = ins[0]
        steps = int(ins[1:])
        if turn == "R":
            direction = Direction((direction.value + 1) % 4)
        else:
            direction = Direction((direction.value - 1) % 4)
        init = curr
        stop = curr
        if i == len(instructions) - 1:
            steps -= 1
        if direction == Direction.NORTH:
            stop = (curr[0], curr[1] - steps)
            end = (curr[0], curr[1] - (steps + 1))
        elif direction == Direction.EAST:
            stop = (curr[0] + steps, curr[1])
            end = (curr[0] + (steps + 1), curr[1])
        elif direction == Direction.SOUTH:
            stop = (curr[0], curr[1] + steps)
            end = (curr[0], curr[1] + (steps + 1))
        elif direction == Direction.WEST:
            stop = (curr[0] - steps, curr[1])
            end = (curr[0] - (steps + 1), curr[1])
        min_wall_x = min(init[0], stop[0])
        max_wall_x = max(init[0], stop[0])
        min_wall_y = min(init[1], stop[1])
        max_wall_y = max(init[1], stop[1])
        maze.append(((min_wall_x, min_wall_y), (max_wall_x, max_wall_y)))
        curr = stop
    # maze.remove(end)
    print("finished parsing")
    # print_maze(maze, start, end, [])
    # min_x = min(pos[0] for pos in maze.union({start, end}))
    # max_x = max(pos[0] for pos in maze.union({start, end}))
    # min_y = min(pos[1] for pos in maze.union({start, end}))
    # max_y = max(pos[1] for pos in maze.union({start, end}))
    # print_maze(maze, start, end, min_x, max_x, min_y, max_y)

    # algo = astar.AStar(
    #     lambda pos: find_neighbours(pos, maze),
    #     lambda a, b: 1,
    #     lambda pos: manhatten_distance(pos, end),
    #     0,
    # )
    algo = dijkstra.Dijkstra(lambda pos: find_neighbours(pos, maze), lambda a, b: 1, 0)
    algo.find_path(start, end)
    print("Result:", algo.get_cost(end))
    # print_maze(maze, start, end, algo.get_path(end))


def print_maze(maze, start, end, path):
    min_x = min(start[0], end[0])
    max_x = max(start[0], end[0])
    min_y = min(start[1], end[1])
    max_y = max(start[1], end[1])

    for wall in maze:
        min_x = min(min_x, wall[0][0], wall[1][0])
        max_x = max(max_x, wall[0][0], wall[1][0])
        min_y = min(min_y, wall[0][1], wall[1][1])
        max_y = max(max_y, wall[0][1], wall[1][1])
    for pos in path:
        min_x = min(min_x, pos[0])
        max_x = max(max_x, pos[0])
        min_y = min(min_y, pos[1])
        max_y = max(max_y, pos[1])

    with open(os.path.join(sys.path[0], "output_maze.txt"), "w", encoding="utf-8") as f:
        for y in range(min_y, max_y + 1):
            line = ""
            for x in range(min_x, max_x + 1):
                pos = (x, y)
                if pos == start:
                    line += "S"
                elif pos == end:
                    line += "E"
                elif pos in path:
                    line += "."
                else:
                    if is_in_wall(pos, maze):
                        line += "#"
                    else:
                        line += " "
            f.write(line + "\n")


def manhatten_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_neighbours(pos, maze):
    neighbours = []
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for delta in deltas:
        new_pos = (pos[0] + delta[0], pos[1] + delta[1])
        if not is_in_wall(new_pos, maze):
            neighbours.append(new_pos)
    return neighbours


def is_in_wall(pos, maze):
    for wall in maze:
        if wall[0][0] <= pos[0] <= wall[1][0] and wall[0][1] <= pos[1] <= wall[1][1]:
            return True
    return False


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
