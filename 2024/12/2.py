import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    
    targets = get_targets(lines)
    
    total = 0
    for distance, height, hardness in targets:
        # calculate C shot
        required_distance = distance - (1-height)
        if required_distance % 3 == 0:
            total += 3 * (required_distance // 3) * hardness
        else:
            required_distance = distance - (0- height)
            if required_distance % 3 == 0:
                total += 2 * (required_distance // 3) * hardness
            else:
                required_distance = distance - (-1-height)
                total += (required_distance // 3) * hardness
    print(total)
            

def get_targets(lines: list[str]):
    targets = []
    for x in range(2, len(lines[0])):
        for y in range(0, len(lines) - 1):
            if lines[y][x] == "T":
                targets.append((x-2, len(lines) - y - 2, 1))
            elif lines[y][x] == "H":
                targets.append((x-2, len(lines) - y - 2, 2))
    return targets

    
if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
