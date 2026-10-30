import os, sys
import time
from functools import cmp_to_key


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    total = 0
    for line in lines:
        compares = [[x[0], x[1], x[2]] for x in line.split(" ")]
        total += compareLine(compares)
    print(total)


def compareLine(compares: list[list[str]]) -> int:
    nums = set()
    compare_hashes: dict[str, tuple[set[str], set[str]]] = dict()
    for a, b, c in compares:
        nums.add(a)
        nums.add(c)
        if a not in compare_hashes:
            compare_hashes[a] = (set(), set())
        if c not in compare_hashes:
            compare_hashes[c] = (set(), set())
        if b == "<":
            compare_hashes[a][1].add(c)
            compare_hashes[c][0].add(a)
        else:
            compare_hashes[a][0].add(c)
            compare_hashes[c][1].add(a)
    num_list = sorted(
        [x for x in nums], key=cmp_to_key(lambda a, b: compare(a, b, compare_hashes))
    )
    return int("".join(num_list))


def compare(a: str, b: str, compares: dict[str, tuple[set[str], set[str]]]) -> int:
    a_hashes = compares[a]
    if b in a_hashes[0]:
        return -1
    if b in a_hashes[1]:
        return 1
    return 0


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
