import os, sys
import time


class Cloud:
    def __init__(self, idx: str, energy: int):
        self.idx = idx
        self.energy = energy
        self.connections: set["Cloud"] = set()

    def add_connection(self, cloud: "Cloud"):
        self.connections.add(cloud)

    def strike(self, damage: int):
        self.energy += damage
        if damage < 2:
            return
        for cloud in self.connections:
            cloud.strike(damage - 1)


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    clouds: dict[str, Cloud] = {}
    for line in lines:
        idx, energy, parts = line.split(", ")
        idx = idx.split("=")[1]
        energy = int(energy.split("=")[1])
        parts = parts.split("=")[1].split(",")
        if idx not in clouds:
            clouds[idx] = Cloud(idx, energy)
        else:
            clouds[idx].energy = energy
        for part in parts:
            if part not in clouds:
                clouds[part] = Cloud(part, 0)
            clouds[idx].add_connection(clouds[part])
    max_connections = 0
    max_cloud = clouds[list(clouds.keys())[0]]
    for cloud in clouds.values():
        if len(cloud.connections) > max_connections:
            max_connections = len(cloud.connections)
            max_cloud = cloud
    max_cloud.strike(5)
    total = 0
    for cloud in clouds.values():
        total += cloud.energy
    print(total)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
