import os, sys
import time


class Branch:
    def __init__(self, size: int, limit: int):
        self.size = size
        self.limit = limit
        self.children: list["Branch"] = []

    def grow(self):
        for child in self.children:
            child.grow()
        # non-splitting
        if (self.size + 1) < self.limit:
            self.size += 1
            return
        # splitting
        self.size = self.size // 2
        left_branch = Branch(self.size, self.limit)
        left_branch.children = self.children
        right_branch = Branch(1, self.limit)
        self.children = [left_branch, right_branch]

    def get_size(self):
        return (
            self.size
            + sum(b.get_size() for b in self.children)
            + (1 if len(self.children) > 0 else 0)
        )


class Plant:
    def __init__(self, idx: str, growth: int, limit: int):
        self.ids = idx
        self.growth = growth
        self.limit = limit
        self.root: "None | Branch" = None

    def count(self):
        return 0 if self.root is None else self.root.get_size()

    def __str__(self):
        if self.root is None:
            return f"Plant {self.ids}: <seed>"

        # Every drawn character is part of the plant: a child branch of size s
        # leaves its parent's "+" diagonally ("\" left, "/" right) and turns
        # vertical ("|") once it has moved far enough sideways to clear its
        # sibling. Its own "+" (if any) may also sit on the diagonal, so it can
        # shift at most s (+1 with children) columns. If that is not enough to
        # clear the sibling, overlapping cells are drawn as "X".
        #
        # layout[id(b)] = (child column offsets, left extent, right extent),
        # all relative to the column of b's "+" (or its tip for a leaf).
        layout: dict[int, tuple[list[int], int, int]] = {}

        def compute(b: Branch) -> tuple[int, int]:
            exts = [compute(c) for c in b.children]
            offsets: list[int] = []
            for i, (c, (l, r)) in enumerate(zip(b.children, exts)):
                if i == 0:
                    need = -(r + 1) if len(exts) > 1 else 0
                elif i == 1:
                    need = l + 1
                else:
                    need = offsets[-1] + exts[i - 1][1] + 2 + l
                reach = c.size + (1 if c.children else 0)
                offsets.append(max(-reach, min(reach, need)))
            left = max([0] + [l - p for p, (l, _) in zip(offsets, exts)])
            right = max([0] + [p + r for p, (_, r) in zip(offsets, exts)])
            layout[id(b)] = (offsets, left, right)
            return left, right

        compute(self.root)
        grid: dict[tuple[int, int], str] = {}

        def put(x: int, y: int, ch: str):
            grid[(x, y)] = "X" if (x, y) in grid else ch

        def draw_children(b: Branch, x: int, top: int):
            """b's "+" is at (x, top); draw its children above it."""
            put(x, top, "+")
            for child, p in zip(b.children, layout[id(b)][0]):
                step = (p > 0) - (p < 0)
                diag = "/" if p > 0 else "\\"
                for j in range(1, child.size + 1):
                    if j <= abs(p):
                        put(x + step * j, top + j, diag)
                    else:
                        put(x + p, top + j, "|")
                if child.children:
                    draw_children(child, x + p, top + child.size + 1)

        root_x = layout[id(self.root)][1]
        for j in range(self.root.size):
            put(root_x, j, "|")
        if self.root.children:
            draw_children(self.root, root_x, self.root.size)
        max_x = max(x for x, _ in grid)
        max_y = max(y for _, y in grid)
        rows = [
            "".join(grid.get((x, y), " ") for x in range(max_x + 1)).rstrip()
            for y in range(max_y, -1, -1)
        ]
        return "\n".join(rows)

    def grow(self):
        if self.count() >= self.limit:
            return True
        # seed initial
        if self.root is None:
            self.root = Branch(1, self.growth)
            return False

        self.root.grow()

        return False


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    total = 0
    for line in lines:
        idx, growth, limit = line.split(", ")
        idx = idx.split("=")[1]
        growth = int(growth.split("=")[1])
        limit = int(limit.split("=")[1])
        plant = Plant(idx, growth, limit)
        count = 0
        while not plant.grow():
            count += 1
            # print(plant)
            # print(count)
        total += count
    print(total)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
