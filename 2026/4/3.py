import os, sys
import time
from functools import cmp_to_key


class Warrior:
    def __init__(self, id: int):
        self.id = id
        self.quests: dict[int, Quest] = {}
        self.points = 0

    def add_part(self, quest: int, part: int, time: int):
        if quest not in self.quests:
            self.quests[quest] = Quest(quest)
        self.quests[quest].set_time(part, time)

    def get_time(self, quest: int, part: int):
        if quest not in self.quests:
            return None
        return self.quests[quest].time(part)

    def award(self, points: int):
        self.points += points

    def get_points(self):
        return self.points


class Quest:
    def __init__(self, id: int):
        self.id = id
        self.part_times: dict[int, int] = {}

    def set_time(self, part: int, time: int):
        self.part_times[part] = time

    def time(self, part: int):
        total = 0
        for i in range(1, part + 1):
            if i not in self.part_times:
                return None
            total += self.part_times[i]
        return total


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    warriors: dict[int, Warrior] = {}
    max_quests = 0
    for line in lines:
        idx, quest, part, time = [int(x.split("=")[1]) for x in line.split(" ")]
        max_quests = max(quest, max_quests)
        if idx not in warriors:
            warriors[idx] = Warrior(idx)
        warriors[idx].add_part(quest, part, time)

    for quest in range(1, max_quests + 1):
        for part in range(1, 4):
            lst: list[tuple[int, Warrior]] = []
            for w in warriors.values():
                w_time = w.get_time(quest, part)
                if w_time is not None:
                    lst.append((w_time, w))
            lst.sort(key=lambda x: x[0])
            points = 50 * part + 1
            running_points = points
            previous_time = 0
            for w in lst:
                points -= 1
                if w[0] > previous_time:
                    running_points = points
                    if points < 1:
                        break
                w[1].award(running_points)
                # print(
                #     "idx:",
                #     w[1].id,
                #     "Quest:",
                #     quest,
                #     "Part:",
                #     part,
                #     "Points:",
                #     running_points,
                # )
                previous_time = w[0]

    final_ranking = sorted(
        [w for w in warriors.values()], key=lambda x: x.get_points(), reverse=True
    )
    total = 0
    running_idx = 0
    previous_points = float("inf")
    for i, w in enumerate(final_ranking):
        # print("Idx:", w.id, "Points:", w.get_points())

        w_points = w.get_points()
        if w_points < previous_points:
            running_idx = i
            previous_points = w_points

        total += (running_idx + 1) * w_points
    print(total)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
