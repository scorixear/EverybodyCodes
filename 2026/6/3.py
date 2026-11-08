import os, sys
import time


class Node:
    def __init__(self, data: str):
        self.data = data
        self.ingredients: set["Node"] = set()

    def add_ingredient(self, ingredient: "Node"):
        self.ingredients.add(ingredient)

    def search(self, visited: set[str]) -> tuple[bool, bool, bool]:
        if self.data == "NULLv1":
            return (True, False, False)
        if self.data == "NULLv2":
            return (False, True, False)
        if self.data == "NULLv3":
            return (False, False, True)
        if self.data in visited:
            return (False, False, False)
        nullv1 = False
        nullv2 = False
        nullv3 = False
        visited.add(self.data)
        for ingredient in self.ingredients:
            result = ingredient.search(visited)
            nullv1 |= result[0]
            nullv2 |= result[1]
            nullv3 |= result[2]
        return (nullv1, nullv2, nullv3)


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    nodes: dict[str, Node] = {}
    for line in lines:
        item, parts = line.split(":")
        if item not in nodes:
            nodes[item] = Node(item)
        for part in parts.split(","):
            if part not in nodes:
                nodes[part] = Node(part)
            nodes[item].add_ingredient(nodes[part])
    count = 0
    for node in nodes.values():
        visited: set[str] = set()
        if node.data == "NULLv1" or node.data == "NULLv2" or node.data == "NULLv3":
            continue
        has_null = node.search(visited)
        if (
            (has_null[0] and has_null[1])
            or (has_null[0] and has_null[2])
            or (has_null[1] and has_null[2])
        ):
            count += 1
    print(count)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
