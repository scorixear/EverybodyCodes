import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    dnas = [line.split(":") for line in lines]
    families = find_child(dnas)
    total = 0
    for child, parent1, parent2 in families.values():
        total += similarity(child[1], parent1[1], parent2[1])
    print(total)


def similarity(child: str, parent1: str, parent2: str) -> int:
    p1_count = 0
    p2_count = 0
    for c, p1, p2 in zip(child, parent1, parent2):
        if c == p1:
            p1_count += 1
        if c == p2:
            p2_count += 1
    return p1_count * p2_count


def find_child(
    dnas: list[list[str]],
) -> dict[str, tuple[list[str], list[str], list[str]]]:
    families: dict[str, tuple[list[str], list[str], list[str]]] = {}
    for i in range(len(dnas)):
        for j in range(i + 1, len(dnas)):
            for k in range(j + 1, len(dnas)):
                is_a = True
                is_b = True
                is_c = True
                for a, b, c in zip(dnas[i][1], dnas[j][1], dnas[k][1]):
                    if a != b and a != c:
                        is_a = False
                    if b != a and b != c:
                        is_b = False
                    if c != a and c != b:
                        is_c = False
                    if not is_a and not is_b and not is_c:
                        break
                if is_a:
                    families[dnas[i][0]] = (dnas[i], dnas[j], dnas[k])
                elif is_b:
                    families[dnas[j][0]] = (dnas[j], dnas[i], dnas[k])
                elif is_c:
                    families[dnas[k][0]] = (dnas[k], dnas[i], dnas[j])
    return families


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
