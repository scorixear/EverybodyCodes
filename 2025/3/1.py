import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    numbers = [int(x) for x in lines[0].split(',')]
    numbers.sort(reverse=True)
    
    curr = numbers[0]
    total_size = curr
    for num in numbers[1:]:
        if num < curr:
            total_size += num
            curr = num
    print(total_size)

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
