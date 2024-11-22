import os, sys
import time

class Node:
    def __init__(self, name: str):
        self.name: str = name
        self.children: list["Node"] = []
        self.parent: "Node" | None = None
    def add_child(self, child: "Node"):
        self.children.append(child)
        if child.parent is None:
            child.parent = self
    def to_root(self, depth, path: list[str]):
        if self.parent is None:
            return (depth, path + [self.name])
        return self.parent.to_root(depth + 1, path + [self.name])
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.__str__()
def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    # list of already created nodes
    nodes: dict[str, Node] = dict()
    # list of leafs (apples)
    apples: list[Node] = []
    # iterate over each edge definition
    for line in lines:
        # the name of the parent node
        name = line.split(":")[0]
        # the children of the parent node
        children = line.split(":")[1].split(",")
        # create the parent node if it doesn't exist
        if name not in nodes:
            nodes[name] = Node(name)
        # iterate over each child
        for child in children:
            childNode = None
            # if the child is an apple
            if child == "@":
                # we do not add it to the nodes list
                # as apples will never be parents
                childNode = Node("@")
                nodes[name].add_child(childNode)
                # add the apple to the apples list
                apples.append(childNode)
                continue
            # if the child is not in the nodes list
            elif child not in nodes:
                # create the child node
                childNode = Node(child)
                nodes[child] = childNode
            # if the child is in the nodes list
            else:
                childNode = nodes[child]
            # add the child to the parent
            nodes[name].add_child(childNode)
    # dictionary of depths and paths with that depth
    depths: dict[int, list[str]] = dict()
    # iterate over each apple
    for apple in apples:
        # get the depth and path to the root
        depth, path = apple.to_root(0, [])
        # if the depth is not in the dictionary
        if depth not in depths:
            # create a new list for that depth
            depths[depth] = []
        # add the path to the list of paths with that depth
        # we reverse the path to get the path from the root to the apple
        # and only take the first character of each nodes name
        depths[depth].append("".join([p[0] for p in path[::-1]]))
    # find the depth that has the least amount of paths
    min_depth = float("inf")
    min_path = ""
    # iterate over each depth
    for depth, paths in depths.items():
        # if the amount of paths is less than the current minimum
        if len(paths) < min_depth:
            # update the minimum depth and path
            min_depth = len(paths)
            min_path = paths
    # print the minimum depth and path
    print(f"Min depth: {min_depth}, Path: {min_path}")
    
if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
