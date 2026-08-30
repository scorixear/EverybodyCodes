import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    total = 0
    for line in lines:
        jumps = [int(x) for x in line.split(",")]
        total += recaman(jumps)
    print(total)


def recaman(jumps: list[int]):
    current = 0
    seen = {0}
    below_arches = []
    above_arches = []
    i = 0
    for j in jumps:
        arches = below_arches
        if i % 2 == 1:
            arches = above_arches
        if (
            current - j >= 0
            and (current - j) not in seen
            and not hasCrossing(j, current, arches, False)
        ):
            current -= j
            seen.add(current)
            arches.append((current, current + j))
            i += 1
        elif not hasAlwaysCrossing(j, current, arches, seen):
            increase_counter = 0
            while (current + j) in seen or hasCrossing(j, current, arches, True):
                j += 1
                increase_counter += 1
                if increase_counter > 100:
                    break
            if increase_counter > 100:
                continue
            current += j
            seen.add(current)
            arches.append((current - j, current))
            i += 1
    # print_arches(current, below_arches, above_arches)
    # print(current, below_arches, above_arches)
    return current


def hasCrossing(
    jump: int,
    current: int,
    arches: list[tuple[int, int]],
    direction: bool,
):
    # looking forward
    if direction:
        for arch in arches:
            if (
                arch[0] < current and arch[1] > current and arch[1] < current + jump
            ) or (
                arch[0] < current + jump
                and arch[0] > current
                and arch[1] > current + jump
            ):
                return True
    # looking backwards
    else:
        for arch in arches:
            if (
                arch[0] > current - jump and arch[0] < current and arch[1] > current
            ) or (
                arch[0] < current - jump
                and arch[1] > current - jump
                and arch[1] < current
            ):
                return True
    return False


def hasAlwaysCrossing(
    jump: int, current: int, arches: list[tuple[int, int]], seen: set[int]
):
    for arch in arches:
        if arch[0] < current and arch[1] > current:
            if arch[1] <= current + jump:
                return True
            allSet = True
            for i in range(current + jump, arch[1]):
                allSet &= i in seen
            return allSet
    return False


def print_arches(
    current: int,
    below_arches: list[tuple[int, int]],
    above_arches: list[tuple[int, int]],
):
    arches = []
    previous = 0
    for i, barch in enumerate(below_arches):
        if barch[0] == previous:
            arches.append(barch)
            previous = barch[1]
        else:
            arches.append((barch[1], barch[0]))
            previous = barch[0]
        if i < len(above_arches):
            aarch = above_arches[i]
            if aarch[0] == previous:
                arches.append(aarch)
                previous = aarch[1]
            else:
                arches.append((aarch[1], aarch[0]))
                previous = aarch[0]
    print(current, arches)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
