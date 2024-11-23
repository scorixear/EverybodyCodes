import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    # the number of priests
    priests = int(lines[0])
    # the number of acolytes
    acolytes = int(lines[1])
    # the number of blocks availabe
    blocks = int(lines[2])
    
    # the number of blocks used
    total_blocks = 1
    # the thickness of the current layer
    current_thickness = 1
    # the maximum height of the structure
    current_height = 1
    # the width of the current layer (increases by 2 with every layer)
    counter = 1
    # while we haven't reached the number of blocks available
    while total_blocks < blocks:
        # increase the width by 2
        counter += 2
        # increase the thickness with the given formula
        current_thickness = (current_thickness * priests) % acolytes
        # we use the current thickness * the width of the current layer blocks with each layer
        total_blocks += current_thickness * counter
        # increase the height of the structure
        current_height += current_thickness
    print(counter * (total_blocks - blocks))
    

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
