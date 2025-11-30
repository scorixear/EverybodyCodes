import os, sys
import time


class Plant:
    def __init__(self, id: int, thickness: int):
        self.id: int = id
        self.free_branches: list[int] = []
        self.thickness: int = thickness
        self.childs: list[tuple["Plant", int]] = []
        self.parents: list[tuple["Plant", int]] = []

    def add_free_branch(self, brightness: int):
        self.free_branches.append(brightness)

    def connect(self, other: "Plant", thickness: int):
        self.childs.append((other, thickness))
        other.parents.append((self, thickness))

    def brightness(self) -> int:
        from_free = sum(self.free_branches)
        from_childs = sum(child[0].brightness() * child[1] for child in self.childs)
        total = from_free + from_childs
        if total < self.thickness:
            return 0
        return total

    def __hash__(self) -> int:
        return hash(self.id)


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    plants: dict[int, Plant] = {}
    in_plant = True
    free_branch_plants = set()
    for line in lines:
        if line == "":
            in_plant = True
            continue
        if in_plant:
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
    print(final_plant.brightness())


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
