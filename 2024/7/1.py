import os, sys
import time

class Chariot:
    def __init__(self, name: str, actions: list[str]):
        self.name: str = name
        self.power: int = 10
        self.total: int = 0
        self.actions: list[str] = actions
    def move(self, segments: int):
        for i in range(segments):
            action = self.actions[i % len(self.actions)]
            if action == "+":
                self.power += 1
            elif action == "-":
                self.power -= 1
                if self.power < 0:
                    self.power = 0
            self.total += self.power
    def __str__(self):
        return f"{self.name}: {self.total}"
    def __repr__(self):
        return self.__str__()

def main():
    with open(os.path.join(sys.path[0],"i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    chariots = []
    for line in lines:
        name = line.split(":")[0]
        actions = line.split(":")[1].split(",")
        chariot = Chariot(name, actions)
        chariot.move(10)
        chariots.append(chariot)
    chariots.sort(key=lambda x: x.total, reverse=True)
    print("".join([chariot.name for chariot in chariots]))

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
