import os, sys
import time


class Hand:
    def __init__(
        self,
        clockwise: bool,
        current: int,
        moves: int,
        number_of_sides: int,
        move_per_side: int,
    ) -> None:
        self.positions = number_of_sides
        self.clockwise = clockwise
        self.current = current * move_per_side
        self.inc = move_per_side
        self.moves = moves

    def __str__(self) -> str:
        return f"{self.positions}, {self.clockwise}, {self.current}, {self.moves}, {self.inc}"

    def __repr__(self) -> str:
        return self.__str__()

    def delta(self):
        if self.moves == 0:
            return 0
        return self.inc if self.clockwise else -self.inc

    def move(self):
        if self.moves == 0:
            return
        if self.clockwise:
            self.current = (self.current + self.inc) % self.positions
        else:
            self.current = (self.current - self.inc) % self.positions
        self.moves -= 1

    def meetings(self, other: "Hand"):
        n = self.positions
        r0 = (other.current - self.current) % n
        rel = other.delta() - self.delta()
        r1 = r0 + rel
        if rel > 0:
            return r1 // n - r0 // n
        if rel < 0:
            return (-r1) // n - (-r0) // n
        return 0


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")

    total = 0
    for i in range(0, len(lines), 5):
        hands: list[Hand] = []
        hand_positions = [int(x) for x in lines[i].split(" ")[1].split(":")]
        directions = [
            True if x == "CW" else False for x in lines[i + 1].split(" ")[1].split(":")
        ]
        current = [int(x) for x in lines[i + 2].split(" ")[1].split(":")]
        move = [int(x) for x in lines[i + 3].split(" ")[1].split(":")]
        largest_common_multiple = lcm(hand_positions)
        largest_moves = 0
        for h, d, c, m in zip(hand_positions, directions, current, move):
            hands.append(
                Hand(d, c, m, largest_common_multiple, largest_common_multiple // h)
            )
            largest_moves = max(largest_moves, m)
        count = 0
        for _ in range(largest_moves):
            hand_copy = [*hands]
            while hand_copy:
                first = hand_copy[0]
                hand_copy = hand_copy[1:]
                for o in hand_copy:
                    count += first.meetings(o)
            for hand in hands:
                hand.move()
        total += count
    print(total)


def lcm(numbers: list[int]) -> int:
    a = numbers[0]
    for b in numbers[1:]:
        a = (a * b) // gcd(a, b)
    return a


def gcd(a, b):
    if a == 0:
        return b
    if b == 0:
        return a
    while b != 0:
        h = a % b
        a = b
        b = h
    return a


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
