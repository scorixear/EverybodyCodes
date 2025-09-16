import os, sys
import time

class Node:
    def __init__(self, rank: int, value: str, id: int):
        self.rank = rank
        self.value = value
        self.level = 0
        self.id = id
        self.left: "Node | None" = None
        self.right: "Node | None" = None
        self.linked: "Node | None" = None
        self.parent: "Node | None" = None
    def add(self, node: "Node"):
        if node.rank < self.rank:
            if self.left:
                return self.left.add(node)
            else:
                self.left = node
                node.parent = self
        elif self.right:
            return self.right.add(node)
        else:
            self.right = node
            node.parent = self
    def get_value(self, level: int):
        if level == 0:
            return [self.value]
        result = []
        if self.left:
            result.extend(self.left.get_value(level - 1))
        if self.right:
            result.extend(self.right.get_value(level - 1))
        return result
    def swap(self):
        if not self.linked:
            raise Exception("Node has no link")
        if not self.parent or not self.linked.parent:
            raise Exception("One of the nodes is root")
        if self.parent.left == self:
            self.parent.left = self.linked
        else:
            self.parent.right = self.linked
        if self.linked.parent.left == self.linked:
            self.linked.parent.left = self
        else:
            self.linked.parent.right = self
        self.parent, self.linked.parent = self.linked.parent, self.parent
        
            

class Tree:
    def __init__(self):
        self.root: Node = Node(0, "", -1)
    def height(self):
        if not self.root:
            return 0
        def calc_height(node):
            if not node:
                return 0
            return max(calc_height(node.left), calc_height(node.right)) + 1
        return calc_height(self.root)
    def add(self, node: Node):
        if not self.root.left:
            self.root.left = node
            node.parent = self.root
        else:
            self.root.left.add(node)
    def get_nodes_per_level(self, level: int):
        if not self.root:
            return []
        return self.root.get_value(level)

def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    left_tree = Tree()
    right_tree = Tree()
    node_list: dict[int, Node] = {}
    for line in lines:
        if line.startswith("ADD"):
            parts = line.split(" ")
            id = int(parts[1].split("=")[1])
            left = parts[2].split("=")[1][1:-1].split(",")
            right = parts[3].split("=")[1][1:-1].split(",")
            left_node = Node(int(left[0]), left[1], id)
            right_node = Node(int(right[0]), right[1], id)
            left_node.linked = right_node
            node_list[id] = left_node
            left_tree.add(left_node)
            right_tree.add(right_node)
        else:
            id = int(line.split(" ")[1])
            node = node_list[id]
            node.swap()
        
    
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
