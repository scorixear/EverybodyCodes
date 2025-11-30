import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    names = lines[0].split(',')
    instructions = [(inst[0], int(inst[1:])) for inst in lines[2].split(',')]
    for dir, step in instructions:
        indx = 0
        if dir == 'R':
            indx = (step) % len(names)
        elif dir == 'L':
            indx = (-step) % len(names)
        names[0], names[indx] = names[indx], names[0]
    print(names[0])

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
