import os, sys
import time
from collections import defaultdict
from dijkstra import Dijkstra


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    portals = int(lines[0].split(": ")[1])
    connections: dict[int, set[int]] = defaultdict(set)
    for line in lines[2:]:
        a, b = line.split(" ")
        a = int(a)
        b = int(b)
        connections[a].add(b)
        connections[b].add(a)

    strain1 = get_strain(portals, {})
    strain2 = get_strain(portals, connections)
    print(strain1 - strain2)


def get_strain(portals: int, connections: dict[int, set[int]]):
    result = 0
    for portal in range(1, portals + 1):
        d = Dijkstra(
            lambda a: get_neighbour(a, portals, connections), lambda a, b: 1, 0
        )
        d.find_path(portal, -1)
        for other in range(1, portals + 1):
            if other == portal:
                continue
            result += d.get_cost(other)
    return result


def get_neighbour(a: int, portals: int, connections: dict[int, set[int]]) -> list[int]:
    result = []
    if a == 1:
        result.append(2)
        result.append(portals)
    elif a == portals:
        result.append(1)
        result.append(portals - 1)
    else:
        result.append(a + 1)
        result.append(a - 1)
    if a not in connections:
        return result
    for conn in connections[a]:
        result.append(conn)
    return result


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
