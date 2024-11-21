import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    runes = lines[0].split(":")[1].split(",")
    
    
    counter = 0
    for line in lines[2:]:
        line_len = len(line)
        prevCounter = counter
        foundIndices = set()
        for rune in runes:
            rune_len = len(rune)
            for i in range(0, line_len - rune_len + 1):
                if line[i:i+rune_len] == rune or line[i:i+rune_len] == rune[::-1]:
                    # print(f"Found {rune} at {i}")
                    for j in range(i, i+rune_len):
                        foundIndices.add(j)
            
        counter += len(foundIndices)
        # print(f"{line} -> {counter - prevCounter}")
    print(counter)
if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")