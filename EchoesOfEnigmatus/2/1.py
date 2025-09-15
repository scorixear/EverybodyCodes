import os, sys
import time

class Node:
    def __init__(self, rank, value):
        self.rank = rank
        self.value = value
        self.left: "Node | None" = None
        self.right: "Node | None" = None
    def get_value(self, counter: int):
        if counter == 0:
            return [self.value]
        result = []
        if self.left:
            result.extend(self.left.get_value(counter - 1))
        if self.right:
            result.extend(self.right.get_value(counter - 1))
        return result
class Tree:
    def __init__(self):
        self.root = None
        self.node_count = 0
        self.max_level = 0
    
    def add(self, rank, value):
        if not self.root:
            self.root = Node(rank, value)
            self.max_level = 1
        else:
            self._add_recursive(self.root, rank, value, 1)
        self.node_count += 1
    def _add_recursive(self, node: Node, rank, value, level: int):
        if rank < node.rank:
            if node.left is None:
                node.left = Node(rank, value)
                self.max_level = max(self.max_level, level + 1)
            else:
                self._add_recursive(node.left, rank, value, level + 1)
        else:
            if node.right is None:
                node.right = Node(rank, value)
                self.max_level = max(self.max_level, level + 1)
            else:
                self._add_recursive(node.right, rank, value, level + 1)
    def get_nodes_per_level(self, level: int):
        if not self.root:
            return []
        return self.root.get_value(level)
        

def main():
    with open(os.path.join(sys.path[0],"i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    left_tree = Tree()
    right_tree = Tree()
    for line in lines:
        parts = line.split(" ")
        left = parts[2].split("=")[1][1:-1].split(",")
        right = parts[3].split("=")[1][1:-1].split(",")
        left_tree.add(int(left[0]), left[1])
        right_tree.add(int(right[0]), right[1])
    
    max_level = max(left_tree.max_level, right_tree.max_level)
    max_node_count = 0
    max_nodes = ""
    for level in range(max_level):
        left_nodes = left_tree.get_nodes_per_level(level)
        right_nodes = right_tree.get_nodes_per_level(level)
        if len(left_nodes) + len(right_nodes) > max_node_count:
            max_node_count = len(left_nodes) + len(right_nodes)
            max_nodes = "".join(left_nodes + right_nodes)
    print(max_nodes)
    

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
