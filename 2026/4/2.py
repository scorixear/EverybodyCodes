import os, sys
import time
from functools import cmp_to_key


class Warrior:
    def __init__(self, id: int):
        self.id = id
        self.quests: dict[int, Quest] = {}

    def add_part(self, quest: int, time: int):
        if quest not in self.quests:
            self.quests[quest] = Quest(quest)
        self.quests[quest].set_time(time)

    def compare(self, other: "Warrior"):
        parts = sum(x.parts() for x in self.quests.values())
        other_parts = sum(x.parts() for x in other.quests.values())
        if parts > other_parts:
            return -1
        if parts < other_parts:
            return 1
        times = sum(x.time() for x in self.quests.values())
        other_times = sum(x.time() for x in other.quests.values())
        if times > other_times:
            return 1
        if times < other_times:
            return -1
        return 0

    def time(self):
        return sum(x.time() for x in self.quests.values())


class Quest:
    def __init__(self, id: int):
        self.id = id
        self.part_times = []

    def set_time(self, time: int):
        self.part_times.append(time)

    def time(self):
        return sum(self.part_times)

    def parts(self):
        return len(self.part_times)


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    warriors: dict[int, Warrior] = {}
    for line in lines:
        idx, quest, part, time = [int(x.split("=")[1]) for x in line.split(" ")]
        if idx not in warriors:
            warriors[idx] = Warrior(idx)
        warriors[idx].add_part(quest, time)
    warrior_lst: list[Warrior] = [w for w in warriors.values()]
    warrior_lst.sort(key=cmp_to_key(lambda a, b: a.compare(b)))
    total = 0
    for i, w in enumerate(warrior_lst):
        total += (i + 1) * w.time()
    print(total)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
