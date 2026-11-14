import os, sys
import time
from collections import defaultdict
from dijkstra import Dijkstra


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
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
    # print(strain1)
    strain2 = get_strain(portals, connections, True)
    # print(strain2)
    print(strain1 - strain2)


def get_strain(portals: int, connections: dict[int, set[int]], with_strain=False):
    min_result = 0
    for portal in range(1, portals + 1):
        d = Dijkstra(
            lambda a: get_neighbour(a, portals, connections, -1, -1),
            lambda a, b: 1,
            0,
        )
        d.find_path(portal, -1)
        for other in range(1, portals + 1):
            if other == portal:
                continue
            min_result += d.get_cost(other)
    if not with_strain:
        return min_result

    for p in range(1, portals + 1):
        for po in range(1, portals + 1):
            if p == po:
                continue
            if mod1(p + 1, portals) == po:
                continue
            if mod1(p + 2, portals) == po:
                continue
            if mod1(p + 3, portals) == po:
                continue
            if mod1(p - 1, portals) == po:
                continue
            if mod1(p - 2, portals) == po:
                continue
            if mod1(p - 3, portals) == po:
                continue
            if p in connections and po in connections[p]:
                continue
            result = 0
            for portal in range(1, portals + 1):
                d = Dijkstra(
                    lambda a: get_neighbour(a, portals, connections, p, po),
                    lambda a, b: 1,
                    0,
                )
                d.find_path(portal, -1)
                for other in range(1, portals + 1):
                    if other == portal:
                        continue
                    result += d.get_cost(other)
            if result < min_result:
                # print(p, po)
                min_result = result
    return min_result


def mod1(a, mod):
    if a > mod:
        return a - mod
    if a < 1:
        return a + mod
    return a


def get_neighbour(
    a: int, portals: int, connections: dict[int, set[int]], add1: int, add2: int
) -> list[int]:
    result = []
    result.append(mod1(a + 1, portals))
    result.append(mod1(a + 2, portals))
    result.append(mod1(a + 3, portals))
    result.append(mod1(a - 1, portals))
    result.append(mod1(a - 2, portals))
    result.append(mod1(a - 3, portals))
    if a == add1:
        result.append(add2)
    elif a == add2:
        result.append(add1)
    if a not in connections:
        return result
    for conn in connections[a]:
        result.append(conn)

    return result


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
