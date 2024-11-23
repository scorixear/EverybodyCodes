import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    # the number of blocks availabe
    blocks = int(lines[0])
    # the number of blocks used
    total_blocks = 0
    # with every layer, (1+layer)*2 blocks are used
    for i  in range(1, blocks, 2):
        # if we exceed the number of blocks available, we print the result and break
        if total_blocks + i > blocks:
            # i = width of the pyramid increases by 2 with every layer
            # total_blocks increases by width with every layer
            print(i * (total_blocks + i - blocks))
            break
        total_blocks += i

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
