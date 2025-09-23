import os, sys
import time
class Dice:
    def __init__(self, id: int, faces: list[int], seed: int):
        self.pulse = seed
        self.seed = seed
        self.faces = faces
        self.id = id
        self.face_id = 0
        self.roll_number = 1
        self.spin = 0
    def roll(self) -> int:
        self.spin = self.roll_number * self.pulse
        self.face_id = (self.face_id + self.spin) % len(self.faces)
        self.pulse += self.spin
        self.pulse %= self.seed
        self.pulse += 1 + self.roll_number + self.seed
        self.roll_number += 1
        return self.faces[self.face_id]

def main():
    with open(os.path.join(sys.path[0],"i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    dices: list[Dice] = []
    for line in lines:
        parts = line.split(" ")
        id = int(parts[0][:-1])
        faces = list(map(int, parts[1].split("=")[1][1:-1].split(",")))
        seed = int(parts[2].split("=")[1])
        dices.append(Dice(id, faces, seed))
    total = 0
    counter = 0
    while total < 10_000:
        dice_total = sum(dice.roll() for dice in dices)
        total += dice_total
        counter += 1
    print(f"Total rolls: {counter}")

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
