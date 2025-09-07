import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    branches = [[(l[0], int(l[1:])) for l in line.split(",")] for line in lines]
    visited = set()
    for branch in branches:
        current = (0,0,0)
        for move in branch:
            match move[0]:
                case "U":
                    visited.update({(current[0], current[1], z) for z in range(current[2] + 1, current[2] + move[1] + 1)})
                    current = (current[0], current[1], current[2] + move[1])
                case "D":
                    visited.update({(current[0], current[1], z) for z in range(current[2] - move[1], current[2])})
                    current = (current[0], current[1], current[2] - move[1])
                case "R":
                    visited.update({(x, current[1], current[2]) for x in range(current[0] + 1, current[0] + move[1] + 1)})
                    current = (current[0] + move[1], current[1], current[2])
                case "L":
                    visited.update({(x, current[1], current[2]) for x in range(current[0] - move[1], current[0])})
                    current = (current[0] - move[1], current[1], current[2])
                case "F":
                    visited.update({(current[0], y, current[2]) for y in range(current[1] + 1, current[1] + move[1] + 1)})
                    current = (current[0], current[1] + move[1], current[2])
                case "B":
                    visited.update({(current[0], y, current[2]) for y in range(current[1] - move[1], current[1])})
                    current = (current[0], current[1] - move[1], current[2])
            # print_grid(visited)
        # print(len(visited))
            # visited.add(current)
    print(len(visited))
    # print_grid(visited)

def print_grid(visited):
    max_x = max(p[0] for p in visited)
    min_x = min(p[0] for p in visited)
    max_y = max(p[1] for p in visited)
    min_y = min(p[1] for p in visited)
    max_z = max(p[2] for p in visited)
    min_z = min(p[2] for p in visited)
    for z in range(max_z, min_z-1, -1):
        for x in range(min_x, max_x + 1):
            if (x, 0, z) in visited:
                print("#", end="")
            else:
                print(".", end="")
        print()

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
