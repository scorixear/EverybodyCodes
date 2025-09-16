import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    snails = []
    for line in lines:
        x, y = map(lambda x: int(x.split("=")[1]), line.split(" "))
        snails.append((x, y))
    
    total = 0
    for snail in snails:
        diag = snail[0] + snail[1] - 1
        left_over = 100%diag
        new_x = (snail[0] + left_over)
        if new_x > diag:
            new_x -= diag
        new_y = (snail[1] - left_over)
        if new_y < 1:
            new_y += diag
        print(new_x, new_y)
        total += new_x + 100*new_y
    print(total)

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
