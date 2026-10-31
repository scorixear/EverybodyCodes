import os, sys
import time


class Warrior:
    def __init__(self, id: int):
        self.id = id
        self.quests: dict[int, Quest] = {}

    def add_part(self, quest: int, part: int, time: int):
        if quest not in self.quests:
            self.quests[quest] = Quest(quest)
        self.quests[quest].set_time(part, time)

    def time(self, quest: int):
        return self.quests[quest].time()


class Quest:
    def __init__(self, id: int):
        self.id = id
        self.part1_time = 0
        self.part2_time = 0
        self.part3_time = 0

    def set_time(self, part: int, time: int):
        if part == 1:
            self.part1_time = time
        elif part == 2:
            self.part2_time = time
        elif part == 3:
            self.part3_time = time

    def time(self):
        return self.part1_time + self.part2_time + self.part3_time


def main():
    with open(os.path.join(sys.path[0], "e1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    warriors: dict[int, Warrior] = {}
    for line in lines:
        idx, quest, part, time = [int(x.split("=")[1]) for x in line.split(" ")]
        if idx not in warriors:
            warriors[idx] = Warrior(idx)
        warriors[idx].add_part(quest, part, time)
    warrior_lst = [w for w in warriors.values()]
    warrior_lst.sort(key=lambda w: w.time(1))
    total = 0
    for i, w in enumerate(warrior_lst):
        total += (i + 1) * w.time(1)
    print(total)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
