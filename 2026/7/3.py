import os, sys
import time


class Cloud:
    def __init__(self, idx: str, energy: int):
        self.idx = idx
        self.energy = energy
        self.exploded = False
        self.connections: set["Cloud"] = set()

    def add_connection(self, cloud: "Cloud"):
        self.connections.add(cloud)

    def strike(self, damage: list[int]):
        for d, count in enumerate(damage):
            if count == 0:
                continue
            self.energy += d * count
        if self.energy > 1000000:
            self.exploded = True

    def get_energy(self) -> int:
        if self.exploded:
            return 0
        return self.energy

    def get_connections(self) -> set["Cloud"]:
        if self.exploded:
            return set()
        return self.connections

    def __repr__(self) -> str:
        return f"(idx={self.idx}, energy={self.energy}, exploded={self.exploded}, connections={[c.idx for c in self.connections]})"

    def __str__(self) -> str:
        return f"(idx={self.idx}, energy={self.energy}, exploded={self.exploded}, connections={[c.idx for c in self.connections]})"


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
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

    max_energy = 0
    start_cloud = clouds[list(clouds.keys())[0]]
    for cloud in clouds.values():
        energy = get_energy(clouds, cloud)
        if energy > max_energy:
            max_energy = energy
            start_cloud = cloud

    print(max_energy, start_cloud.idx)


def get_energy(origin: dict[str, Cloud], origin_cloud: Cloud) -> int:
    clouds = {}
    for idx, cloud in origin.items():
        clouds[idx] = Cloud(cloud.idx, cloud.energy)
    for idx, cloud in origin.items():
        for connection in cloud.connections:
            clouds[idx].add_connection(clouds[connection.idx])
    start_cloud = clouds[origin_cloud.idx]
    queue: dict[str, tuple[list[int], Cloud]] = {
        start_cloud.idx: ([0] * 10 + [1], start_cloud)
    }
    stage_count = 1
    while len(queue) > 0:
        # print_queue(stage_count, queue)
        stage_count += 1
        new_queue: dict[str, tuple[list[int], Cloud]] = {}
        for strikes, cloud in queue.values():
            if not any(strikes):
                continue
            new_strikes = []
            was_exploded = cloud.exploded
            cloud.strike(strikes)
            new_strikes = [0] + strikes[2:] + [0]
            if cloud.exploded:
                if not was_exploded:
                    for connection in cloud.connections:
                        if connection.exploded:
                            continue
                        if connection.idx not in new_queue:
                            new_queue[connection.idx] = ([0] * 10 + [1], connection)
                        else:
                            new_queue[connection.idx][0][10] += 1
                        for s, i in enumerate(new_strikes):
                            new_queue[connection.idx][0][s] += i
                continue
            for connection in cloud.get_connections():
                if connection.exploded:
                    continue
                if connection.idx not in new_queue:
                    new_queue[connection.idx] = ([x for x in new_strikes], connection)
                else:
                    for s, i in enumerate(new_strikes):
                        new_queue[connection.idx][0][s] += i
        queue = new_queue
    return sum(cloud.get_energy() for cloud in clouds.values())


def print_queue(stage_count: int, queue: dict[str, tuple[list[int], Cloud]]):
    print(f"Stage: {stage_count} {len(queue)}")
    if len(queue) == 37:
        print(f"Queue: {queue}")
    queue_idx = sorted(queue.keys(), key=lambda x: int(x))
    for idx in queue_idx:
        strikes, cloud = queue[idx]
        strike_count: dict[int, int] = {}
        for strike in strikes:
            if strike not in strike_count:
                strike_count[strike] = 0
            strike_count[strike] += 1
        for strike, count in sorted(strike_count.items(), key=lambda x: x[0]):
            print(
                f"cloud {cloud.idx} received {count} impulsed with strength {strike} (energy {cloud.energy})"
            )


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
