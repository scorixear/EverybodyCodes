import os, sys
import time
import itertools

def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    columns = [[] for _ in range(len(lines[0]))]
    sequences = []
    read_grid = True
    for y, line in enumerate(lines):
        if line == "":
            read_grid = False
            continue
        if read_grid:
            for x, c in enumerate(line):
                if c == "*":
                    columns[x].append(y)
        else:
            sequences.append(list(line))
    
    total = 0
    dp = {}
    for x in range(0, len(columns), 2):
        for sequence in sequences:
            key = (x,) + tuple(sequence)
            result = play(x, sequence, columns)
            dp[key] = result

    perms = itertools.permutations(range(0, len(columns), 2), len(sequences))
    max_coins = 0
    min_coins = float('inf')
    for perm in perms:
        total = 0
        for i, start_x in enumerate(perm):
            sequence = sequences[i]
            key = (start_x,) + tuple(sequence)
            total += dp[key]
        min_coins = min(min_coins, total)
        max_coins = max(max_coins, total)
   
    print(min_coins)
    print(max_coins)

def play(start_x, sequence, columns):
    pos_x = start_x
    pos_y = 0
    for i, c in enumerate(sequence):
        next_y = find_next_y(columns, pos_x, pos_y)
        if next_y is None:
            final_slot = pos_x//2+1
            return max(0, (final_slot*2) - (start_x//2+1))
        if c == "L":
            if pos_x == 0:
                pos_x +=1
            else:
                pos_x -= 1
        elif c == "R":
            if pos_x == len(columns)-1:
                pos_x -= 1
            else:
                pos_x += 1
        pos_y = next_y
    final_slot = pos_x//2+1
    return max(0, (final_slot*2) - (start_x//2+1))
def find_next_y(columns, x, y):
    col = columns[x]
    for cy in col:
        if cy >= y:
            return cy
    return None

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
