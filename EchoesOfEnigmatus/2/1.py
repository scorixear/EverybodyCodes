import os, sys
import time

class Node:
    def __init__(self, rank, value):
        self.rank = rank
        self.value = value
        self.left: "Node | None" = None
        self.right: "Node | None" = None
        self.level = 0
    def add(self, node: "Node") -> int:
        if node.rank < self.rank:
            if self.left:
                return self.left.add(node)
            else:
                self.left = node
                node.level = self.level + 1
                return node.level
        elif self.right:
            return self.right.add(node)
        else:
            self.right = node
            node.level = self.level + 1
            return node.level
    def get_value(self, level: int):
        if level == 0:
            return [self.value]
        result = []
        if self.left:
            result.extend(self.left.get_value(level - 1))
        if self.right:
            result.extend(self.right.get_value(level - 1))
        return result
class Tree:
    def __init__(self):
        self.root = None
    def height(self):
        if not self.root:
            return 0
        def calc_height(node):
            if not node:
                return 0
            return max(calc_height(node.left), calc_height(node.right)) + 1
        return calc_height(self.root)
    def add(self, node: Node):
        if not self.root:
            self.root = node
        else:
            self.root.add(node)
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
        left_node = Node(int(left[0]), left[1])
        right_node = Node(int(right[0]), right[1])
        left_tree.add(left_node)
        right_tree.add(right_node)

    max_level = max(left_tree.height(), right_tree.height())
    max_node_count_left = 0
    max_node_count_right = 0
    max_nodes_left = ""
    max_nodes_right = ""
    for level in range(max_level):
        left_nodes = left_tree.get_nodes_per_level(level)
        right_nodes = right_tree.get_nodes_per_level(level)
        if len(left_nodes) > max_node_count_left:
            max_node_count_left = len(left_nodes)
            max_nodes_left = "".join(left_nodes)
        if len(right_nodes) > max_node_count_right:
            max_node_count_right = len(right_nodes)
            max_nodes_right = "".join(right_nodes)
    print(max_nodes_left + max_nodes_right)
    

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
