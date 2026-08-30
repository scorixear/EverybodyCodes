import os, sys
import time


class Tile:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.top = False
        self.right = False
        self.bottom = False
        self.left = False

    def is_isolated(self) -> bool:
        return self.top and self.right and self.bottom and self.left


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    grid: list[list[Tile]] = []
    width = int(lines[0].split("=")[1])
    height = int(lines[1].split("=")[1])
    for y in range(height):
        row = []
        for x in range(width):
            row.append(Tile(x, y))
        grid.append(row)

    horizontal = lines[2].split("=")[1]
    vertical = lines[3].split("=")[1]
    for x in range(width):
        c1 = vertical[x % len(vertical)]
        c2 = vertical[(x + 1) % len(vertical)]
        for y in range(height):
            if y % 2 == 0:
                if c1 == "0":
                    grid[y][x].left = True
                if c2 == "0":
                    grid[y][x].right = True
            else:
                if c1 == "1":
                    grid[y][x].left = True
                if c2 == "1":
                    grid[y][x].right = True
    for y in range(height):
        c1 = horizontal[y % len(horizontal)]
        c2 = horizontal[(y + 1) % len(horizontal)]
        for x in range(width):
            if x % 2 == 0:
                if c1 == "0":
                    grid[y][x].top = True
                if c2 == "0":
                    grid[y][x].bottom = True
            else:
                if c1 == "1":
                    grid[y][x].top = True
                if c2 == "1":
                    grid[y][x].bottom = True
    print_grid(grid)
    total_isolated = 0
    for y in range(height):
        for x in range(width):
            if grid[y][x].is_isolated():
                total_isolated += 1
                # print(y, x)
    print(total_isolated)


def print_grid(grid: list[list[Tile]]):
    for y in range(len(grid)):
        row = grid[y]
        top_border = ""
        line = ""
        for x in range(len(row)):
            tile = row[x]
            if tile.top:
                top_border += " -"
            else:
                top_border += "  "
            if tile.left:
                line += "| "
            else:
                line += "  "
        last_tile = row[len(row) - 1]
        top_border += " "
        if last_tile.right:
            line += "|"
        else:
            line += " "
        print(top_border)
        print(line)
    last_row = grid[len(grid) - 1]
    line = ""
    for x in range(len(last_row)):
        tile = last_row[x]
        if tile.bottom:
            line += " -"
        else:
            line += "  "
    line += " "
    print(line)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
