import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    columns = [int(x) for x in lines[0].split(",")]
    numbers = identify_spell(columns)
    # print(",".join(str(x) for x in numbers))
    total_blocks = 202520252025000

    left, right = 0, total_blocks * 2

    while left < right:
        mid = (left + right + 1) // 2
        blocks_used = calculate_blocks_used(numbers, mid)

        if blocks_used <= total_blocks:
            left = mid
        else:
            right = mid - 1
    print(left)


def calculate_blocks_used(numbers: list[int], up_to_column: int) -> int:
    total = 0
    for num in numbers:
        total += up_to_column // num
    return total


def identify_spell(columns: list[int]):
    numbers = []
    for i in range(0, len(columns)):
        fits = True
        new_columns = columns.copy()
        for j in range(i, len(columns), i + 1):
            if columns[j] == 0:
                fits = False
                break
            new_columns[j] -= 1
        if fits:
            numbers.append(i + 1)
            columns = new_columns
    return numbers


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
