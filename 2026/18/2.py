import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    rows: dict[int, tuple[int, int]] = {}
    max_y = 0
    for line in lines:
        x, y, w = [int(l.split("=")[1]) for l in line.split(" ")]
        max_y = max(y, max_y)
        for d in range(y):
            if d not in rows:
                rows[d] = (x, x + w - 1)
            else:
                rows[d] = (min(rows[d][0], x), max(rows[d][1], x + w - 1))

    count = 0
    for y in range(max_y):
        count += rows[y][1] - rows[y][0] + 1
    # print(rows)
    print(count)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
