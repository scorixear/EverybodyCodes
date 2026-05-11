import os, sys
import time


class Node:
    def __init__(
        self,
        id: int,
        plug: tuple[str, str],
        leftSocket: tuple[str, str],
        rightSocket: tuple[str, str],
        data,
    ):
        self.id = id
        self.plug = plug
        self.leftSocket = leftSocket
        self.left: "Node | None" = None
        self.rightSocket = rightSocket
        self.right: "Node | None" = None
        self.data = data

    def addNode(self, other: "Node"):
        if self.left is None:
            if self.leftSocket == other.plug:
                self.left = other
                return True
            elif self.right is None:
                if self.rightSocket == other.plug:
                    self.right = other
                    return True
                else:
                    return False
            else:
                return self.right.addNode(other)
        elif self.left.addNode(other):
            return True
        elif self.right is None:
            if self.rightSocket == other.plug:
                self.right = other
                return True
            else:
                return False
        else:
            return self.right.addNode(other)

    def __str__(self):
        return f"{self.id}"

    def __repr__(self):
        return self.__str__()


class Tree:
    def __init__(self):
        self.root = None

    def addNode(self, node: Node):
        if self.root is None:
            self.root = node
            return True
        return self.root.addNode(node)

    def getData(self) -> list:
        data = []
        if self.root is None:
            return data

        def dfs(node: Node):
            if node.left is not None:
                dfs(node.left)
            data.append(node.id)
            if node.right is not None:
                dfs(node.right)

        dfs(self.root)
        return data


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    tree = Tree()
    for line in lines:
        id, plug, leftSocket, rightSocket, data = line.split(",")
        id_parsed = int(id.strip().split("=")[1])
        plug_parsed = (
            plug.strip().split("=")[1].split(" ")[0],
            plug.strip().split("=")[1].split(" ")[1],
        )
        leftSocket_parsed = (
            leftSocket.strip().split("=")[1].split(" ")[0],
            leftSocket.strip().split("=")[1].split(" ")[1],
        )
        rightSocket_parsed = (
            rightSocket.strip().split("=")[1].split(" ")[0],
            rightSocket.strip().split("=")[1].split(" ")[1],
        )
        data_parsed = data.strip().split("=")[1]
        tree.addNode(
            Node(
                id_parsed,
                plug_parsed,
                leftSocket_parsed,
                rightSocket_parsed,
                data_parsed,
            )
        )
    tree_data = tree.getData()
    result = sum((i + 1) * x for i, x in enumerate(tree_data))
    print(result)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
