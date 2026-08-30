import os, sys
import time

if sys.platform == "win32":
    os.system("")  # enable ANSI escape processing on Windows consoles
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]  # box-drawing chars need utf-8, not cp1252

RESET = "\033[0m"
BORDER = "\033[91m"  # red
FILL_COLORS_VIVID = {
    False: "\033[48;5;46m",
    True: "\033[48;5;226m",
}  # bright green/yellow bg, isolated tiles
FILL_COLORS_DIM = {
    False: "\033[48;5;22m",
    True: "\033[48;5;58m",
}  # muted green/olive bg, everything else

# indexed by (north, south, east, west) segment presence at a grid corner
BOX_CHARS = {
    (False, False, False, False): " ",
    (False, False, False, True): "╴",
    (False, False, True, False): "╶",
    (False, False, True, True): "─",
    (False, True, False, False): "╷",
    (False, True, False, True): "┐",
    (False, True, True, False): "┌",
    (False, True, True, True): "┬",
    (True, False, False, False): "╵",
    (True, False, False, True): "┘",
    (True, False, True, False): "└",
    (True, False, True, True): "┴",
    (True, True, False, False): "│",
    (True, True, False, True): "┤",
    (True, True, True, False): "├",
    (True, True, True, True): "┼",
}


class Tile:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.top = False
        self.right = False
        self.bottom = False
        self.left = False
        self.Color: bool | None = None

    def is_isolated(self) -> bool:
        return self.top and self.right and self.bottom and self.left


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
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
    for y in range(height):
        for x in range(width):
            tile = grid[y][x]
            if tile.Color is not None:
                continue
            if tile.left and x > 0:
                tile.Color = not grid[y][x - 1].Color
            elif not tile.left and x > 0:
                tile.Color = grid[y][x - 1].Color
            elif tile.top and y > 0:
                tile.Color = not grid[y - 1][x].Color
            elif not tile.top and y > 0:
                tile.Color = grid[y - 1][x].Color
            else:
                tile.Color = False

    # print_grid(grid)
    isolated_group_true = 0
    isolated_group_false = 0
    for y in range(height):
        for x in range(width):
            if grid[y][x].is_isolated():
                if grid[y][x].Color:
                    isolated_group_true += 1
                else:
                    isolated_group_false += 1
                # print(y, x)
    print(max(isolated_group_false, isolated_group_true))


def print_grid(grid: list[list[Tile]]):
    height = len(grid)
    width = len(grid[0])

    # horizontal segment between corners (i, j) and (i+1, j), i in [0, width), j in [0, height]
    def h_exists(i: int, j: int) -> bool:
        return grid[j][i].top if j < height else grid[j - 1][i].bottom

    # vertical segment between corners (i, j) and (i, j+1), i in [0, width], j in [0, height)
    def v_exists(i: int, j: int) -> bool:
        return grid[j][i].left if i < width else grid[j][width - 1].right

    def corner(i: int, j: int) -> str:
        n = j > 0 and v_exists(i, j - 1)
        s = j < height and v_exists(i, j)
        w = i > 0 and h_exists(i - 1, j)
        e = i < width and h_exists(i, j)
        char = BOX_CHARS[(n, s, e, w)]
        return f"{BORDER}{char}{RESET}" if char != " " else " "

    def h_seg(i: int, j: int) -> str:
        return f"{BORDER}──{RESET}" if h_exists(i, j) else "  "

    def v_seg(i: int, j: int) -> str:
        return f"{BORDER}│{RESET}" if v_exists(i, j) else " "

    def fill(tile: Tile) -> str:
        assert tile.Color is not None
        colors = FILL_COLORS_VIVID if tile.is_isolated() else FILL_COLORS_DIM
        return f"{colors[tile.Color]}  {RESET}"

    for j in range(height):
        border_row = "".join(corner(i, j) + h_seg(i, j) for i in range(width)) + corner(
            width, j
        )
        tile_row = "".join(
            v_seg(i, j) + fill(grid[j][i]) for i in range(width)
        ) + v_seg(width, j)
        print(border_row)
        print(tile_row)

    bottom_row = "".join(
        corner(i, height) + h_seg(i, height) for i in range(width)
    ) + corner(width, height)
    print(bottom_row)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
