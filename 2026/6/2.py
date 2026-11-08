import os, sys
import time


class Node:
    def __init__(self, data: str):
        self.data = data
        self.ingredients: set["Node"] = set()

    def add_ingredient(self, ingredient: "Node"):
        self.ingredients.add(ingredient)

    def search(self, visited: dict[str, bool]) -> bool:
        if self.data == "NULL":
            return True
        if self.data in visited:
            return visited[self.data]
        visited[self.data] = False
        for ingredient in self.ingredients:
            if ingredient.search(visited):
                visited[self.data] = True
                break
        return visited[self.data]


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
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
    visited = {}
    for node in nodes.values():
        if node.data == "NULL":
            continue
        node.search(visited)
    count = sum(1 for has_null in visited.values() if has_null)
    print(count)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
