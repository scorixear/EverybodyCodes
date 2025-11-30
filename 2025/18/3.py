import os, sys
import time


class Plant:
    def __init__(self, id: int, thickness: int):
        self.id: int = id
        self.free_branches: list[int] = []
        self.thickness: int = thickness
        self.childs: list[tuple["Plant", int]] = []
        self.parents: list[tuple["Plant", int]] = []
        self.dp_entry: set[int] = set()

    def add_free_branch(self, brightness: int):
        self.free_branches.append(brightness)
        self.dp_entry = set([self.id])

    def is_all_positive(self) -> bool:
        for _, thickness in self.parents:
            if thickness < 0:
                return False
        return True

    def is_all_negative(self) -> bool:
        for _, thickness in self.parents:
            if thickness > 0:
                return False
        return True

    def connect(self, other: "Plant", thickness: int):
        self.childs.append((other, thickness))
        other.parents.append((self, thickness))
        self.dp_entry = set()
        for child, _ in self.childs:
            self.dp_entry.update(child.dp_entry)

    def get_dp_entry(self, case: dict[int, bool]):
        key = set()
        for id in self.dp_entry:
            if id in case and case[id]:
                key.add(id)
        return (self.id, frozenset(key))

    def brightness(self, case: dict[int, bool], dp: dict) -> int:
        dp_key = self.id
        if dp_key in dp:
            return dp[dp_key]
        from_free = 0
        if self.id in case and case[self.id]:
            from_free = sum(self.free_branches)
        from_childs = sum(
            child[0].brightness(case, dp) * child[1] for child in self.childs
        )
        total = from_free + from_childs
        if total < self.thickness:
            total = 0
        dp[dp_key] = total
        return total

    def __hash__(self) -> int:
        return hash(self.id)


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    plants: dict[int, Plant] = {}
    in_plant = True
    in_cases = False
    free_branch_plants = set()
    cases = []
    for line in lines:
        if line == "":
            if in_plant:
                in_plant = False
                in_cases = True
            else:
                in_plant = True
            continue
        if in_cases:
            parts = {}
            for i, part in enumerate(line.split(" ")):
                parts[i + 1] = part == "1"
            cases.append(parts)
        elif in_plant:
            parts = line.split(" ")
            id = int(parts[1])
            thickness = int(parts[4][:-1])
            plants[id] = Plant(id, thickness)
            in_plant = False
        else:
            parts = line.split(" ")
            if parts[1] == "free":
                thickness = int(parts[5])
                plants[id].add_free_branch(thickness)
                free_branch_plants.add(plants[id])
            else:
                other_id = int(parts[4])
                thickness = int(parts[7])
                plants[id].connect(plants[other_id], thickness)
    final_plant = None
    for plant in plants.values():
        if len(plant.parents) == 0:
            final_plant = plant
            break
    assert final_plant is not None

    for plant in free_branch_plants:
        assert plant.is_all_positive() or plant.is_all_negative()

    max_case = {plant.id: plant.is_all_positive() for plant in free_branch_plants}
    max_brightness = final_plant.brightness(max_case, {})

    print(max_brightness)
    total = 0
    for case in cases:
        result = final_plant.brightness(case, {})
        if result == 0:
            continue
        total += max_brightness - result
    print(total)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
