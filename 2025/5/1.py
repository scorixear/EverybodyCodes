import os, sys
import time

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.center = None
    def add(self, value):
        if value < self.value:
            if self.left is None:
                self.left = value
                return
        elif value > self.value:
            if self.right is None:
                self.right = value
                return
        if self.center is None:
            self.center = Node(value)
            return
        self.center.add(value)
    def get_center(self):
        center = self.center
        values = str(self.value)
        while center is not None:
            values += str(center.value)
            center = center.center
        return int(values)

def main():
    with open(os.path.join(sys.path[0],"i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    numbers = [int(x) for x in lines[0].split(':')[1].split(',')]
    root = Node(numbers[0])
    for number in numbers[1:]:
        root.add(number)
    print(root.get_center())

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
