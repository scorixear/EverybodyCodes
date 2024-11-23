import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    # the number of priests
    priests = int(lines[0])
    # the number of acolytes
    acolytes = int(lines[1])
    # the number of blocks availabe
    blocks = int(lines[2])
    # blocks = 202400000000
    # the height of each column
    heights = [1]
    # the thickness of the current layer
    thickness = 1
    # the total number of blocks used
    total_blocks = 1
    # the width of the current structure
    width = 1
    # while we haven't reached the number of blocks available
    while total_blocks < blocks:
        # increase the thickness with the given formula
        thickness = (thickness * priests) % acolytes + acolytes
        # increase the width by 2
        width += 2
        # add the height of the current layer to the list
        heights.insert(0, 0)
        heights.append(0)
        # increase the height of each column by the thickness
        for i in range(len(heights)):
            heights[i] += thickness
        # calculate the total number of blocks used without holes
        num_blocks = sum(heights)
        # precalculate the number of blocks that need to be removed
        temp = priests * width
        # remove blocks from each column except the first and last
        for i in range(1, len(heights) - 1):
            # use the given formula
            removed_blocks = (temp * heights[i]) % acolytes
            # remove the blocks
            num_blocks -= removed_blocks
        # the total number of blocks used is the sum of the heights - the removed blocks
        total_blocks = num_blocks
    print(total_blocks - blocks)
        

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
