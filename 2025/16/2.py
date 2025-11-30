import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    columns = [int(x) for x in lines[0].split(",")]
    total = 1
    for i in range(0, len(columns)):
        fits = True
        new_columns = columns.copy()
        for j in range(i, len(columns), i + 1):
            if columns[j] == 0:
                fits = False
                break
            new_columns[j] -= 1
        if fits:
            total *= i + 1
            columns = new_columns
    print(total)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
