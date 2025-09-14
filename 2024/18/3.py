import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    original_pines = set()
    original_channel = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "P":
                original_pines.add((x, y))
            elif c == ".":
                original_channel.add((x, y))
    score = float('inf')
    total_amount_channels = len(original_channel)
    curr_channel_count = 0  
    for x, y in original_channel:
        curr_channel_count += 1
        print(f"Calculating ({curr_channel_count}/{total_amount_channels})")
        # print(f"Starting at {(x, y)}")
        pines = original_pines.copy()
        channel = original_channel.copy()
        water = set()
        water.add((x, y))
        channel.remove((x, y))
        counter = 0
        total = 0
        while pines:
            to_be_added = set()
            found_pines = 0
            for x, y in water:
                dd = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                for dx, dy in dd:
                    if (x + dx, y + dy) in channel:
                        channel.remove((x + dx, y + dy))
                        to_be_added.add((x + dx, y + dy))
                    elif (x + dx, y + dy) in pines:
                        found_pines += 1
                        pines.remove((x + dx, y + dy))
                        to_be_added.add((x + dx, y + dy))
            water = to_be_added
            counter += 1
            total += found_pines * counter
            # print(found_pines, counter, total)
        score = min(score, total)
        # print(total)
    print(score)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
