import os, sys
import time
import dijkstra


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    expanded_grid = [[], []]
    volcano = (0, 0)
    start = (0, 0, 0)
    end = (0, 0, 1)
    for i, line in enumerate(lines):
        row = []
        row2 = []
        for j, char in enumerate(line):
            if char == "@":
                row.append(0)
                row2.append(0)
                volcano = (j, i)
            elif char == "S":
                row.append(0)
                row2.append(0)
                start = (j, i, 0)
                end = (j, i, 1)
            else:
                row.append(int(char))
                row2.append(int(char))
        expanded_grid[0].append(row)
        expanded_grid[1].append(row2)
    curr_radius = 0
    while True:
        algo = create_dijkstra(curr_radius, expanded_grid, volcano)
        algo.find_path(start, end)
        cost = algo.get_cost(end)
        print("Checked radius", curr_radius, "with cost", cost)
        # print_path(expanded_grid[0], algo.get_path(end))
        if cost < (curr_radius + 1) * 30:
            print("Result:", cost, "at radius", curr_radius)
            print(cost * curr_radius)
            break
        curr_radius += 1


def print_path(grid: list[list[int]], path: list[tuple[int, int, int]]):
    print()
    path_set = set((x, y) for x, y, _ in path)
    for y in range(len(grid)):
        row = ""
        for x in range(len(grid[0])):
            if (x, y) in path_set:
                row += "."
            else:
                row += str(grid[y][x])
        print(row)
    print()


def create_dijkstra(radius: int, grid: list[list[list[int]]], volcano: tuple[int, int]):
    return dijkstra.Dijkstra(
        lambda pos: get_neighbours(pos, radius, grid, volcano),
        lambda a, b: grid[0][b[1]][b[0]],
        0,
    )


def get_neighbours(
    pos: tuple[int, int, int],
    radius: int,
    grid: list[list[list[int]]],
    volcano: tuple[int, int],
) -> list[tuple[int, int, int]]:
    neighbours = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    squared_radius = radius**2
    for d in directions:
        new_x = pos[0] + d[0]
        new_y = pos[1] + d[1]
        if 0 <= new_x < len(grid[0][0]) and 0 <= new_y < len(grid[0]):
            dist = (volcano[0] - new_x) ** 2 + (volcano[1] - new_y) ** 2
            if dist <= squared_radius or (new_x, new_y) == volcano:
                continue
            if (
                pos[2] == 1
                and new_y > volcano[1]
                and new_x < volcano[0]
                and pos[0] >= volcano[0]
            ):
                neighbours.append((new_x, new_y, 0))
            elif (
                pos[2] == 0
                and new_y > volcano[1]
                and new_x >= volcano[0]
                and pos[0] < volcano[0]
            ):
                neighbours.append((new_x, new_y, 1))
            # elif pos[2] == 0 and new_x >= volcano[0] and new_y < volcano[1]:
            #     continue
            # elif pos[2] == 1 and new_x < volcano[0] and new_y < volcano[1]:
            #     continue
            else:
                neighbours.append((new_x, new_y, pos[2]))
    return neighbours


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
