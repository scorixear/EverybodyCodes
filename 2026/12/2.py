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
        min_spells = min(width, height)
        if l_width == 0 or l_height == 0:
            return min_spells
        return min(min_spells, width - l_width + height - l_height)


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
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
