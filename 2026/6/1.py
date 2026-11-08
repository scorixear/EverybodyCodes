import os, sys
import time


class Node:
    def __init__(self, data: str):
        self.data = data
        self.ingredients: set["Node"] = set()

    def add_ingredient(self, ingredient: "Node"):
        self.ingredients.add(ingredient)

    def search(self, visited: set[str]) -> set[str]:
        if self.data in visited:
            return set()
        visited.add(self.data)
        for ingredient in self.ingredients:
            visited |= ingredient.search(visited)
        return visited


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
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
    null_node = nodes["NULL"]
    ingredients = null_node.search(set())
    print(len(ingredients) - 1)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
