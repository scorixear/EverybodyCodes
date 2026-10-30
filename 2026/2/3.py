import os, sys
import time


class Node:
    def __init__(self, val: str):
        self.val = val
        self.left = []
        self.right = []

    def add_left(self, node: "Node"):
        self.left.append(node)

    def add_right(self, node: "Node"):
        self.right.append(node)

    def get_left(self, visited: set["Node"]):
        for n in self.left:
            if n in visited:
                continue
            visited.add(n)
            n.get_left(visited)

    def count_left(self):
        visited = set()
        self.get_left(visited)
        return len(visited)


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    total = 0
    for line in lines:
        compares = [[x[0], x[1], x[2]] for x in line.split(" ")]
        total += compareLine(compares)
    print(total)


def compareLine(compares: list[list[str]]) -> int:
    nums: dict[str, Node] = dict()
    for a, b, c in compares:
        if a not in nums:
            nums[a] = Node(a)
        if c not in nums:
            nums[c] = Node(c)
    for a, b, c in compares:
        if b == ">":
            nums[c].add_left(nums[a])
            nums[a].add_right(nums[c])
        else:
            nums[a].add_left(nums[c])
            nums[c].add_right(nums[a])
    nodes = sorted([x for x in nums.values()], key=lambda x: x.count_left())
    result = "".join([n.val for n in nodes])
    return int(result)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
