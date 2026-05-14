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

    def _place_in_slot(
        self,
        socket: tuple[str, str],
        child: "Node | None",
        is_strong: bool,
        other: "Node",
    ) -> tuple["Node | None", bool, "Node | None"]:
        # if the slot is empty
        # we can potentially place the new node here
        if child is None:
            # if the new node doesn't bond with the socket
            if not self.is_bond(socket, other.plug):
                # it cannot be placed
                # the child doesn't change, the bond doesn't change, the displaced node is the new node
                return child, is_strong, other
            # if the new node can form a bond
            # it could be placed here
            # the child becomes the new node, the bond is updated, the displaced node is None
            return other, self.is_strong_bond(socket, other.plug), None
        # the slot is not empty
        # if this is not a strong bond, and the new node can form a strong bond
        if not is_strong and self.is_strong_bond(socket, other.plug):
            # the new node takes the slot, the bond becomes strong, the displaced node is the old child
            return other, True, child
        # the child bond is already strong or the new node cannot form a strong bond
        # the child doesn't change, the bond doesn't change,
        # the displaced node is the result of trying to place the new node in the child
        return child, is_strong, child.addNode(other)

    def addNode(self, other: "Node") -> "Node | None":
        # try to place the new node in the left slot
        self.left, self.leftStrong, displaced = self._place_in_slot(
            self.leftSocket, self.left, self.leftStrong, other
        )
        # if the node was added to the left, we are done
        if displaced is None:
            return None
        # otherwise add the displaced node to the right slot (this might still be the original node)
        self.right, self.rightStrong, displaced = self._place_in_slot(
            self.rightSocket, self.right, self.rightStrong, displaced
        )
        return displaced

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
            return
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
