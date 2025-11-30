import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    numbers = set([int(x) for x in lines[0].split(',')])
    numbers = list(sorted(numbers))
    next_crate(numbers, 20, 0, 0)
    
def next_crate(crates: list[int], target: int, sum: int, crate_count: int) -> bool:
    if len(crates) == 0:
        if crate_count == target:
            print(sum)
            return True
    if crate_count > target:
        return False
    if crate_count + 1 == target:
        print(sum + crates[0])
        return True
    for i in range(len(crates)):
        next_crates = []
        if i > 0:
            next_crates += crates[0:i]
        if i + 1 < len(crates):
            next_crates += crates[i+1:]
        if next_crate(next_crates, target, sum + crates[i], crate_count + 1):
            return True
    return False
        
    
if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
