import os, sys
import time
from itertools import combinations


class Piece:
    def __init__(self, id: int, char: str):
        self.id = id
        self.char = char
        # neighbour piece id -> number of borders shared with that piece
        self.neighbours: dict[int, int] = {}

    def add_neighbour(self, other: "Piece"):
        self.neighbours[other.id] = self.neighbours.get(other.id, 0) + 1


def build_pieces(grid: list[str]) -> list[Piece]:
    height, width = len(grid), len(grid[0])

    # 1. flood fill: label every cell with the id of its piece
    ids = [[-1] * width for _ in range(height)]
    # piece 0 is the outer frame: it is a neighbour of every piece on the edge
    frame = Piece(0, "#")
    pieces: list[Piece] = [frame]
    for sy in range(height):
        for sx in range(width):
            if ids[sy][sx] != -1:
                continue
            piece = Piece(len(pieces), grid[sy][sx])
            pieces.append(piece)
            ids[sy][sx] = piece.id
            stack = [(sx, sy)]
            while stack:
                x, y = stack.pop()
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if (
                        0 <= nx < width
                        and 0 <= ny < height
                        and ids[ny][nx] == -1
                        and grid[ny][nx] == piece.char
                    ):
                        ids[ny][nx] = piece.id
                        stack.append((nx, ny))

    # 2. count borders. Each cell only looks right and down, so every border
    #    is seen exactly once and gets added to both pieces.
    for y in range(height):
        for x in range(width):
            p = pieces[ids[y][x]]
            # outer borders: one per side of the cell that lies on the grid edge
            # (a corner cell touches the frame twice)
            on_edge = (y == 0) + (y == height - 1) + (x == 0) + (x == width - 1)
            for _ in range(on_edge):
                p.add_neighbour(frame)
                frame.add_neighbour(p)

            for nx, ny in ((x + 1, y), (x, y + 1)):
                if nx < width and ny < height and ids[ny][nx] != p.id:
                    q = pieces[ids[ny][nx]]
                    p.add_neighbour(q)
                    q.add_neighbour(p)

    return pieces


def min_spanning_tree(pieces: list[Piece], charged: set[int] = set()) -> int:
    """
    Kruskal with union-find over the piece graph.
    Every edge touching a charged piece is free (weight 0).
    """
    edges = [
        (0 if piece.id in charged or other in charged else weight, piece.id, other)
        for piece in pieces
        for other, weight in piece.neighbours.items()
        if piece.id < other  # each edge is stored on both pieces, take it once
    ]
    edges.sort()

    parent = list(range(len(pieces)))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = 0
    for weight, a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            total += weight
    return total


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        grid = f.read().strip().split("\n")

    pieces = build_pieces(grid)

    # try every pair of real pieces (id 0 is the frame, it can't be charged)
    # and keep the pair that gives the cheapest spanning tree
    best = min_spanning_tree(pieces)
    best_pair = None
    for a, b in combinations(range(1, len(pieces)), 2):
        cost = min_spanning_tree(pieces, {a, b})
        if cost < best:
            best, best_pair = cost, (pieces[a].char, pieces[b].char)
    print(best, best_pair)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
