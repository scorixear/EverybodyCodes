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
    def compare(self, other:'Node') -> int:
        curr_value_str = ""
        if self.left is not None:
            curr_value_str += str(self.left)
        curr_value_str += str(self.value)
        if self.right is not None:
            curr_value_str += str(self.right)
        curr_value = int(curr_value_str)
        other_value_str = ""
        if other.left is not None:
            other_value_str += str(other.left)
        other_value_str += str(other.value)
        if other.right is not None:
            other_value_str += str(other.right)
        other_value = int(other_value_str)
        if curr_value > other_value:
            return 1
        if curr_value < other_value:
            return -1
        if self.center is None and other.center is None:
            return 0
        if self.center is None:
            return -1
        if other.center is None:
            return 1
        return self.center.compare(other.center)
            

def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    swords = []
    for line in lines:
        id, numbers = line.split(':')
        numbers = [int(x) for x in numbers.split(',')]
        root = Node(numbers[0])
        for number in numbers[1:]:
            root.add(number)
        quality = root.get_center()
        sorted_insert(swords, quality, int(id), root)
    
    total = 0
    for i in range(len(swords)):
        pos = i + 1
        total += pos * swords[i][0]
    print(total)
        
def sorted_insert(swords: list[tuple[int, int, Node]], quality: int, id: int, root: Node):
    for i in range(len(swords)):
        other_id, other_quality, other_root = swords[i]
        if quality > other_quality:
            swords.insert(i, (id, quality, root))
            return
        if quality == other_quality:
            root_compare = root.compare(other_root)
            if root_compare > 0:
                swords.insert(i, (id, quality, root))
                return
            if root_compare == 0:
                if id > other_id:
                    swords.insert(i, (id, quality, root))
                    return
    swords.append((id, quality, root))


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
