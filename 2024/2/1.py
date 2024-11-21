import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    runes = lines[0].split(":")[1].split(",")
    
    
    counter = 0
    for rune in runes:
        counter += lines[2].count(rune)
    print(counter)
if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")