import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"input.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        counter = 0
        for char in text:
            if char == 'B':
                counter += 1
            elif char == 'C':
                counter += 3
        print(counter)
        
if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
