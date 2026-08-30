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
        self.Color: bool | None = None

    def is_isolated(self) -> bool:
        return self.top and self.right and self.bottom and self.left


def residue_counts(n: int, period: int) -> list[int]:
    # how many x in [0, n) fall on each x % period residue
    full, rem = divmod(n, period)
    counts = [full] * period
    for r in range(rem):
        counts[r] += 1
    return counts


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    width = int(lines[0].split("=")[1])
    height = int(lines[1].split("=")[1])
    horizontal = lines[2].split("=")[1]
    vertical = lines[3].split("=")[1]

    # The border/color pattern repeats exactly every 2*len(vertical) columns
    # and every 2*len(horizontal) rows (a full period of border crossings
    # always flips the running color parity by an even amount), so we only
    # need to simulate one such tile and multiply by how often each cell
    # inside it recurs across the full width/height.
    period_x = min(2 * len(vertical), width)
    period_y = min(2 * len(horizontal), height)
    column_counts = residue_counts(width, period_x)
    row_counts = residue_counts(height, period_y)

    isolated_group_true = 0
    isolated_group_false = 0
    previous_row = []
    previous_cell = Tile(0, 0)
    for y in range(period_y):
        row = []
        top = horizontal[y % len(horizontal)]
        bottom = horizontal[(y + 1) % len(horizontal)]
        multiplier_y = row_counts[y]
        for x in range(period_x):
            left = vertical[x % len(vertical)]
            right = vertical[(x + 1) % len(vertical)]
            tile = Tile(x, y)

            # Border Decision
            if y % 2 == 0:
                if left == "0":
                    tile.left = True
                if right == "0":
                    tile.right = True
            else:
                if left == "1":
                    tile.left = True
                if right == "1":
                    tile.right = True
            if x % 2 == 0:
                if top == "0":
                    tile.top = True
                if bottom == "0":
                    tile.bottom = True
            else:
                if top == "1":
                    tile.top = True
                if bottom == "1":
                    tile.bottom = True

            # Color Decision
            if tile.left and x > 0:
                tile.Color = not previous_cell.Color
            elif not tile.left and x > 0:
                tile.Color = previous_cell.Color
            elif tile.top and y > 0:
                tile.Color = not previous_row[x].Color
            elif not tile.top and y > 0:
                tile.Color = previous_row[x].Color
            else:
                tile.Color = False

            # Isolation Count, scaled by how often this (x % period_x, y % period_y) cell recurs
            if tile.is_isolated():
                count = column_counts[x] * multiplier_y
                if tile.Color:
                    isolated_group_true += count
                else:
                    isolated_group_false += count
            row.append(tile)
            previous_cell = tile
        previous_row = row

    print(max(isolated_group_false, isolated_group_true))


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
