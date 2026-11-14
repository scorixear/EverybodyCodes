import os, sys
import time


class Stack:
    def __init__(self):
        self.cells: set[tuple[int, int]] = set()

    def add_cell(self, x, y):
        self.cells.add((x, y))

    def get_min_x(self):
        return min(c[0] for c in self.cells)

    def get_max_x(self):
        return max(c[0] for c in self.cells)

    def get_min_y(self):
        return min(c[1] for c in self.cells)

    def get_max_y(self):
        return max(c[1] for c in self.cells)

    def get_width(self):
        return self.get_max_x() - self.get_min_x() + 1

    def get_height(self):
        return self.get_max_y() - self.get_min_y() + 1

    def get_box(self):
        min_x = self.get_min_x()
        max_x = self.get_max_x()
        min_y = self.get_min_y()
        max_y = self.get_max_y()
        # find start empty
        startx, starty = None, None
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if (x, y) not in self.cells:
                    startx, starty = x, y
                    break
            if startx is not None:
                break
        if startx is None or starty is None:
            return 0, 0, 0, 0, 0, 0
        queue = [(startx, starty)]
        seen = set()
        min_b_x = float("inf")
        max_b_x = 0
        min_b_y = float("inf")
        max_b_y = 0
        while queue:
            x, y = queue.pop(0)
            if (x, y) in seen:
                continue
            min_b_x = min(min_b_x, x)
            max_b_x = max(max_b_x, x)
            min_b_y = min(min_b_y, y)
            max_b_y = max(max_b_y, y)
            seen.add((x, y))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if nx == min_x or nx == max_x or ny == min_y or ny == max_y:
                    if (nx, ny) not in self.cells:
                        return 0, 0, 0, 0, 0, 0
                if (nx, ny) not in self.cells:
                    queue.append((nx, ny))
        return (
            max_b_x - min_b_x + 1,  # width
            max_b_y - min_b_y + 1,  # height
            min_b_x - min_x,  # border left
            max_x - max_b_x,  # border right
            min_b_y - min_y,  # border top
            max_y - max_b_y,  # border bottom
        )

    def get_l_width(self):
        min_x = self.get_min_x()
        max_x = self.get_max_x()
        min_y = self.get_min_y()
        max_y = self.get_max_y()
        initial_width = 0
        for x in range(min_x, max_x + 1):
            if (x, min_y) in self.cells:
                initial_width += 1
        for y in range(min_y + 1, max_y + 1):
            row_width = 0
            for x in range(min_x, max_x + 1):
                if (x, y) in self.cells:
                    row_width += 1
            if row_width != initial_width:
                return abs(row_width - initial_width)
        return 0

    def get_l_height(self):
        min_x = self.get_min_x()
        max_x = self.get_max_x()
        min_y = self.get_min_y()
        max_y = self.get_max_y()
        initial_height = 0
        for y in range(min_y, max_y + 1):
            if (min_x, y) in self.cells:
                initial_height += 1
        for x in range(min_x + 1, max_x + 1):
            column_height = 0
            for y in range(min_y, max_y + 1):
                if (x, y) in self.cells:
                    column_height += 1
            if column_height != initial_height:
                return abs(column_height - initial_height)
        return 0

    def spell_cost(self):
        width = self.get_width()
        height = self.get_height()
        l_width = self.get_l_width()
        l_height = self.get_l_height()
        b_width, b_height, b_b_l, b_b_r, b_b_t, b_b_b = self.get_box()
        min_spells = min(width, height)
        if (l_width == 0 or l_height == 0) and (b_width == 0 or b_height == 0):
            return min_spells
        if b_width == 0 or b_height == 0:
            return min(min_spells, width - l_width + height - l_height)
        # remove around
        h_base = height - b_height

        # left border
        if b_b_l < b_height:
            h_base += b_b_l
        else:
            h_base += b_height
        # right border
        if b_b_r < b_height:
            h_base += b_b_r
        else:
            h_base += b_height

        w_base = width - b_width
        # top border
        if b_b_t < b_width:
            w_base += b_b_t
        else:
            w_base += b_width
        if b_b_b < b_width:
            w_base += b_b_b
        else:
            w_base += b_width
        return min(w_base, h_base)


def main():
    with open(
        os.path.join(sys.path[0], "i3.txt"),
        "r",
        encoding="utf-8",
    ) as f:
        text = f.read().strip()
        lines = text.split("\n")
    seen: set[tuple[int, int]] = set()
    stacks: list[Stack] = []
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == ".":
                continue
            if (x, y) in seen:
                continue
            stacks.append(flood_fill(x, y, lines, seen))
    count = 0
    # print(stacks)
    for stack in stacks:
        count += stack.spell_cost()
    print(count)


def flood_fill(startx, starty, grid, seen) -> Stack:
    width = len(grid[0])
    height = len(grid)
    queue = [(startx, starty)]
    stack = Stack()
    while queue:
        x, y = queue.pop(0)
        if (x, y) in seen:
            continue
        seen.add((x, y))
        stack.add_cell(x, y)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == "#":
                queue.append((nx, ny))
    return stack


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
