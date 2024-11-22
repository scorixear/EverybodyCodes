import os, sys
import time

class Chariot:
    def __init__(self, name: str, actions: list[str]):
        self.name: str = name
        self.power: int = 10
        self.total: int = 0
        self.actions: list[str] = actions
    def move(self, track: list[str]):
        for i in range(len(track) * 10):
            action = self.actions[i % len(self.actions)]
            track_action = track[(i+1) % len(track)]
            if track_action == "=" or track_action == "S":
                if action == "+":
                    self.power += 1
                elif action == "-":
                    self.power -= 1
                    if self.power < 0:
                        self.power = 0
            elif track_action == "+":
                self.power += 1
            elif track_action == "-":
                self.power -= 1
                if self.power < 0:
                    self.power = 0
            self.total += self.power
    def __str__(self):
        return f"{self.name}: {self.total}"
    def __repr__(self):
        return self.__str__()

def main():
    with open(os.path.join(sys.path[0],"i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    with open(os.path.join(sys.path[0],"i2t.txt"), "r", encoding="utf-8") as f:
        track_lines = f.read().strip().split("\n")
    track = []
    for i in range(len(track_lines[0])):
        track.append(track_lines[0][i])
    for i in range(1, len(track_lines)):
        track.append(track_lines[i][-1])
    for i in range(len(track_lines[0])-2, -1, -1):
        track.append(track_lines[-1][i])
    for i in range(len(track_lines)-2, 0, -1):
        track.append(track_lines[i][0])
    print(track)
    
    chariots = []
    for line in lines:
        name = line.split(":")[0]
        actions = line.split(":")[1].split(",")
        chariot = Chariot(name, actions)
        chariot.move(track)
        chariots.append(chariot)
    chariots.sort(key=lambda x: x.total, reverse=True)
    print("".join([chariot.name for chariot in chariots]))

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
