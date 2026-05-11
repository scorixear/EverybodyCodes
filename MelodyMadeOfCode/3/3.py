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
        self.leftStrong = False
        self.rightSocket = rightSocket
        self.right: "Node | None" = None
        self.rightStrong = False
        self.data = data

    @staticmethod
    def is_strong_bond(socket: tuple[str, str], plug: tuple[str, str]) -> bool:
        return socket[0] == plug[0] and socket[1] == plug[1]

    @staticmethod
    def is_bond(socket: tuple[str, str], plug: tuple[str, str]) -> bool:
        return socket[0] == plug[0] or socket[1] == plug[1]

    def addNode(self, other: "Node") -> "Node | None":
        # Is left node empty
        if self.left is None:
            # is there any match
            if self.is_bond(self.leftSocket, other.plug):
                # we will add it
                # is it a strong bond
                if self.is_strong_bond(self.leftSocket, other.plug):
                    self.leftStrong = True
                self.left = other
                return None
            # there is no match, try right node
            # is right node empty
            if self.right is None:
                # is there any match
                if self.is_bond(self.rightSocket, other.plug):
                    # we will add it
                    # is it a strong bond
                    if self.is_strong_bond(self.rightSocket, other.plug):
                        self.rightStrong = True
                    self.right = other
                    return None
                # there is no match, we can't add it
                return other
            # right node is not empty
            # is it already a strong bond
            if self.rightStrong:
                # add it to the right node
                return self.right.addNode(other)
            # its not already a strong bond
            # is this a strong bond
            if self.is_strong_bond(self.rightSocket, other.plug):
                # we overpower it
                self.rightStrong = True
                newOther = self.right
                self.right = other
                # new overpowered should continue next node after this one
                return newOther
            # right node is not empty,
            # its either already a strong bond
            # or this is not a strong bond
            # we add it to the right node
            return self.right.addNode(other)
        # left node is not empty
        # is it already a strong bond
        if self.leftStrong:
            # we try to add it to the left node
            newOther = self.left.addNode(other)
            # did it succeed
            if newOther is None:
                return None
            # it did not succeed or it returned a new node to add
            # is the right slot empty
            if self.right is None:
                # is it any match
                if self.is_bond(self.rightSocket, newOther.plug):
                    # we will add it
                    # is it a strong bond
                    if self.is_strong_bond(self.rightSocket, newOther.plug):
                        self.rightStrong = True
                    self.right = newOther
                    return None
                # there is no match, we can't add it
                return newOther
            # right slot is not empty
            # is it already a strong bond
            if self.rightStrong:
                # we add it to the right node
                return self.right.addNode(newOther)
            # its not already a strong bond
            # is this a strong bond
            if self.is_strong_bond(self.rightSocket, newOther.plug):
                # we overpower it
                self.rightStrong = True
                newOther2 = self.right
                self.right = newOther
                # new overpowered should continue next node after this one
                return newOther2
            # right node is not empty,
            # its either already a strong bond
            # or this is not a strong bond
            # we add it to the right node
            return self.right.addNode(newOther)
        # left node is not empty, but its not a strong bond
        # is this a strong bond
        if self.is_strong_bond(self.leftSocket, other.plug):
            # we overpower it
            self.leftStrong = True
            newOther = self.left
            self.left = other
            # new other should try right node
            # is right slot empty
            if self.right is None:
                # is there any match
                if self.is_bond(self.rightSocket, newOther.plug):
                    # we will add it
                    # is it a strong bond
                    if self.is_strong_bond(self.rightSocket, newOther.plug):
                        self.rightStrong = True
                    self.right = newOther
                    return None
                # there is no match, we can't add it
                return newOther
            # right slot is not empty
            # is it already a strong bond
            if self.rightStrong:
                # we add it to the right node
                return self.right.addNode(newOther)
            # its not already a strong bond
            # is this a strong bond
            if self.is_strong_bond(self.rightSocket, newOther.plug):
                # we overpower it
                self.rightStrong = True
                newOther2 = self.right
                self.right = newOther
                # new overpowered should continue next node after this one
                return newOther2
            # right node is not empty,
            # its either already a strong bond
            # or this is not a strong bond
            # we add it to the right node
            return self.right.addNode(newOther)
        # left node is not empty
        # its either already a strong bond
        # or this is not a strong bond
        # we try to add it to the left node
        newOther = self.left.addNode(other)
        # did it succeed
        if newOther is None:
            return None
        # it did not succeed or it returned a new node to add
        # is the right slot empty
        if self.right is None:
            # is it any match
            if self.is_bond(self.rightSocket, newOther.plug):
                # we will add it
                # is it a strong bond
                if self.is_strong_bond(self.rightSocket, newOther.plug):
                    self.rightStrong = True
                self.right = newOther
                return None
            # there is no match, we can't add it
            return newOther
        # right slot is not empty
        # is it already a strong bond
        if self.rightStrong:
            # we add it to the right node
            return self.right.addNode(newOther)
        # its not already a strong bond
        # is this a strong bond
        if self.is_strong_bond(self.rightSocket, newOther.plug):
            # we overpower it
            self.rightStrong = True
            newOther2 = self.right
            self.right = newOther
            # new overpowered should continue next node after this one
            return newOther2
        # right node is not empty,
        # its either already a strong bond
        # or this is not a strong bond
        # we add it to the right node
        return self.right.addNode(newOther)

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
        nodeToAdd = node
        while nodeToAdd is not None:
            nodeToAdd = self.root.addNode(nodeToAdd)

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
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
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
