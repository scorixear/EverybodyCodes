import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    mentors: dict[str, list[int]] = {}
    novices: dict[str, list[int]] = {}
    for i, char in enumerate(lines[0]):
        if char.upper() == char:
            mentors[char] = mentors.get(char, [])
            mentors[char].append(i)
        else:
            novices[char] = novices.get(char, [])
            novices[char].append(i)
    result = 0
    tents = len(lines[0])
    max_distance = 1000
    repeat_times = 1000
    for novice_char, novice_positions in novices.items():
        mentor_char = novice_char.upper()
        if mentor_char not in mentors:
            continue
        mentor_positions = mentors[mentor_char]
        total = 0
        for novice_pos in novice_positions:
            novice_total = 0
            for mentor_pos in mentor_positions:
                if mentor_pos < novice_pos and novice_pos - mentor_pos <= max_distance:
                    novice_total += repeat_times
                    continue
                if mentor_pos > novice_pos and mentor_pos - novice_pos <= max_distance:
                    novice_total += repeat_times
                    continue
                if (
                    mentor_pos > novice_pos
                    and novice_pos < max_distance
                    and novice_pos + (tents - mentor_pos) <= max_distance
                ):
                    novice_total += repeat_times - 1
                    continue
                if (
                    mentor_pos < novice_pos
                    and (tents - novice_pos) < max_distance
                    and (tents - novice_pos) + mentor_pos <= max_distance
                ):
                    novice_total += repeat_times - 1
                    continue
            print(mentor_char, novice_char, novice_pos, novice_total)
            total += novice_total
        result += total
    print(result)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
