import os, sys
import time

GREY = "\033[90m"
RESET = "\033[0m"


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    width = len(lines[0])
    height = len(lines)
    gaps = set(
        (x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == "."
    )
    start: tuple[int, int] = (0, 0)

    queue: list[tuple[int, int]] = [start]
    seen = set()
    count = 0
    while queue:
        x, y = queue.pop(0)
        if (x, y) in seen:
            continue
        seen.add((x, y))
        for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in gaps:
                queue.append((nx, ny))
            else:
                count += 1
    print(count)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
