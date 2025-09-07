import os, sys
import time

class Coord:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x}, {self.y})"
def score(catapult: int, power: int) -> int:
    return (catapult+1) * power

def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    meteorites = [Coord(int(line.split(" ")[0]), int(line.split(" ")[1])) for line in lines]
    total = 0
    for meteor in meteorites:
        minScore = float('inf')
        for i in range(3):
            can_intercept, currScore = try_intercept(meteor, i)
            if can_intercept:
                minScore = min(minScore, currScore)
        print(minScore)
        total += minScore
    print(total)

def try_intercept(meteor: Coord, catapult: int) -> tuple[bool, int]:
    if meteor.x % 2 == 1:
        meteor = Coord(meteor.x - 1, meteor.y - 1)

    x = meteor.x // 2
    # Step 1: if Meteor.x - Meteor.y + offset == 0,
    # then you get it on the upswing, and power is Meteor.x / 2
    if meteor.x - meteor.y + catapult == 0:
        power = x
        return True, score(catapult, power)
    
    # Step 2: y == bc == p + offset equation
    # at x, y will have dropped by x amount
    y = meteor.y - x
    power = y - catapult
    if power <= x <= power * 2:
        return True, score(catapult, power)

    # Step 3: Apply formula from pts 1 + 2.
    adjX = x + y - catapult
    if adjX % 3 == 0 and y - catapult <= x:
        power = adjX // 3
        return True, score(catapult, power)
    return False, -1
    

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
