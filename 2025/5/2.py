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
    with open(os.path.join(sys.path[0],"i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    max_sword = 0
    min_sword = float('inf')
    for line in lines:
        numbers = [int(x) for x in line.split(':')[1].split(',')]
        root = Node(numbers[0])
        for number in numbers[1:]:
            root.add(number)
        quality = root.get_center()
        if quality > max_sword:
            max_sword = quality
        if quality < min_sword:
            min_sword = quality
        
    
    print(max_sword - min_sword)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
