import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    names = lines[0].split(',')
    instructions = [(inst[0], int(inst[1:])) for inst in lines[2].split(',')]
    curr = 0
    for dir, step in instructions:
        if dir == 'R':
            curr  = (curr + step) % len(names)
        elif dir == 'L':
            curr = (curr - step) % len(names)
    print(names[curr])

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
