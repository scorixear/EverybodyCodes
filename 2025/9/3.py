import os, sys
import time


class Node:
    def __init__(self, name: str):
        self.name = int(name)
        self.children: list["Node"] = []
        self.parents: list["Node"] = []

    def add_child(self, child: "Node"):
        self.children.append(child)
        child.parents.append(self)

    def visit(self, visited: set["Node"]):
        if self in visited:
            return
        visited.add(self)
        for child in self.children:
            child.visit(visited)
        for parent in self.parents:
            parent.visit(visited)

    def __hash__(self) -> int:
        return hash(self.name)


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    dnas = [line.split(":") for line in lines]
    families = find_child(dnas)
    nodes: dict[str, Node] = {}
    for child, (parent1, parent2) in families.items():
        if parent1 not in nodes:
            nodes[parent1] = Node(parent1)
        if parent2 not in nodes:
            nodes[parent2] = Node(parent2)
        if child not in nodes:
            nodes[child] = Node(child)
        nodes[parent1].add_child(nodes[child])
        nodes[parent2].add_child(nodes[child])

    total_visited = set()
    max_size = 0
    max_value = 0
    for node in nodes.values():
        if node in total_visited:
            continue
        visited = set()
        node.visit(visited)
        total_visited.update(visited)
        family_value = sum(n.name for n in visited)
        # print(len(visited), family_value)
        if len(visited) > max_size:
            max_size = len(visited)
            max_value = family_value
    print(max_value)


def find_child(
    dnas: list[list[str]],
) -> dict[str, tuple[str, str]]:
    families: dict[str, tuple[str, str]] = {}
    for i in range(len(dnas)):
        for j in range(i + 1, len(dnas)):
            for k in range(j + 1, len(dnas)):
                is_a = True
                is_b = True
                is_c = True
                for a, b, c in zip(dnas[i][1], dnas[j][1], dnas[k][1]):
                    if a != b and a != c:
                        is_a = False
                    if b != a and b != c:
                        is_b = False
                    if c != a and c != b:
                        is_c = False
                    if not is_a and not is_b and not is_c:
                        break
                if is_a:
                    families[dnas[i][0]] = (dnas[j][0], dnas[k][0])
                elif is_b:
                    families[dnas[j][0]] = (dnas[i][0], dnas[k][0])
                elif is_c:
                    families[dnas[k][0]] = (dnas[i][0], dnas[j][0])
    return families


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
