import os, sys
import time
from collections import defaultdict
from dijkstra import Dijkstra


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
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
            lambda a: get_neighbour(a, portals, connections, {}),
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

    spacing = portals // 8
    for start in range(1, 1 + spacing, 1):
        additional_portals = set(
            [x for x in range(start, start + 8 * spacing, spacing)]
        )
        a1 = additional_portals.pop()
        seen: set[
            tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]
        ] = set()
        for a2 in additional_portals:
            if already_connected(a1, a2, portals, connections):
                continue
            for b1 in additional_portals.difference(set([a2])):
                for b2 in additional_portals.difference(set([a2, b1])):
                    if already_connected(b1, b2, portals, connections):
                        continue
                    for c1 in additional_portals.difference(set([a2, b1, b2])):
                        for c2 in additional_portals.difference(set([a2, b1, b2, c1])):
                            if already_connected(c1, c2, portals, connections):
                                continue
                            for d1 in additional_portals.difference(
                                set([a2, b1, b2, c1, c2])
                            ):
                                d2 = additional_portals.difference(
                                    set([a2, b1, b2, c1, c2, d1])
                                ).pop()
                                if already_connected(d1, d2, portals, connections):
                                    continue
                                add: dict[int, int] = {}
                                pairs = sorted(
                                    [
                                        (min(a1, a2), max(a1, a2)),
                                        (min(b1, b2), max(b1, b2)),
                                        (min(c1, c2), max(c1, c2)),
                                        (min(d1, d2), max(d1, d2)),
                                    ],
                                    key=lambda x: x[0],
                                )
                                if (pairs[0], pairs[1], pairs[2], pairs[3]) in seen:
                                    continue
                                seen.add((pairs[0], pairs[1], pairs[2], pairs[3]))
                                add[a1] = a2
                                add[a2] = a1
                                add[b1] = b2
                                add[b2] = b1
                                add[c1] = c2
                                add[c2] = c1
                                add[d1] = d2
                                add[d2] = d1
                                result = 0
                                for portal in range(1, portals + 1):
                                    d = Dijkstra(
                                        lambda a: get_neighbour(
                                            a, portals, connections, add
                                        ),
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


def already_connected(a, b, portals, connections):
    if a == b:
        return True
    if mod1(a + 1, portals) == b:
        return True
    if mod1(a + 2, portals) == b:
        return True
    if mod1(a + 3, portals) == b:
        return True
    if mod1(a - 1, portals) == b:
        return True
    if mod1(a - 2, portals) == b:
        return True
    if mod1(a - 3, portals) == b:
        return True
    if a in connections and b in connections[a]:
        return True
    return False


def mod1(a, mod):
    if a > mod:
        return a - mod
    if a < 1:
        return a + mod
    return a


def get_neighbour(
    a: int, portals: int, connections: dict[int, set[int]], add: dict[int, int]
) -> list[int]:
    result = []
    result.append(mod1(a + 1, portals))
    result.append(mod1(a + 2, portals))
    result.append(mod1(a + 3, portals))
    result.append(mod1(a - 1, portals))
    result.append(mod1(a - 2, portals))
    result.append(mod1(a - 3, portals))
    if a in add:
        result.append(add[a])
    if a not in connections:
        return result
    for conn in connections[a]:
        result.append(conn)

    return result


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
