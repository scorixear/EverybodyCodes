import os, sys
import time

sys.path.append(os.path.join(sys.path[0], "..", ".."))
from algorithms.astar import AStar

GREY = "\033[90m"
RESET = "\033[0m"


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    width = len(lines[0])
    height = len(lines)
    gaps = set(
        (x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == "."
    )
    start: tuple[int, int] = (0, 0)
    end: tuple[int, int] = (width - 1, height - 1)

    def neighbour(a: tuple[int, int]) -> list[tuple[int, int]]:
        result = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = a[0] + dx, a[1] + dy
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in gaps:
                result.append((nx, ny))
        return result

    def cost(a: tuple[int, int], b: tuple[int, int]) -> int:
        return 1

    def heuristic(a: tuple[int, int]) -> int:
        return end[0] - a[0] + end[1] - a[1]

    alg = AStar(neighbour, cost, heuristic, 0)
    alg.find_path(start, end)
    print(alg.get_cost(end))
    print_grid(lines, alg.get_path(end))


def print_grid(grid: list[str], path: list[tuple[int, int]]):
    for y, row in enumerate(grid):
        row_line = ""
        for x, c in enumerate(row):
            if (x, y) not in path:
                row_line += f"{GREY}{c}{RESET}"
            else:
                row_line += c
        print(row_line)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
