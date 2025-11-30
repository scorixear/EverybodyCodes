import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    dnas = [line.split(":")[1] for line in lines]
    child, parents = find_child(dnas)
    p1_counter = 0
    p2_counter = 0
    for c, p1, p2 in zip(child, parents[0], parents[1]):
        if c == p1:
            p1_counter += 1
        if c == p2:
            p2_counter += 1
    print(p1_counter * p2_counter)


def find_child(dnas: list[str]) -> tuple[str, list[str]]:
    is_a = True
    is_b = True
    is_c = True
    for a, b, c in zip(dnas[0], dnas[1], dnas[2]):
        # assuem a = child
        if a != b and a != c:
            is_a = False
        # assume b == child
        if b != a and b != c:
            is_b = False
        # assume c == child
        if c != a and c != b:
            is_c = False

        if not is_a and not is_b:
            return dnas[2], [dnas[0], dnas[1]]
        if not is_a and not is_c:
            return dnas[1], [dnas[0], dnas[2]]
        if not is_b and not is_c:
            return dnas[0], [dnas[1], dnas[2]]
    return dnas[0], [dnas[1], dnas[2]]  # default return, should not reach here


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
