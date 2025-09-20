import os, sys
import time
from collections import deque

def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    balloons = list(map(lambda x: 0 if x == "R" else 1 if x == "G" else 2, lines[0])) * 100_000
    
    # Split the balloons into two deques
    first_half = deque()
    second_half = deque(balloons)
    
    current_shot = 0
    shot_count = 0
    
    while first_half or second_half:
        shot_count += 1
        
        # Check total length before removing anything
        total_len = len(first_half) + len(second_half)
        
        # Get the first balloon
        if first_half:
            current_balloon = first_half.popleft()
        else:
            current_balloon = second_half.popleft()
        
        # Check if we need to remove the middle element (based on length before removing first)
        if current_balloon == current_shot and total_len % 2 == 0 and total_len > 0:
            # Calculate middle position (after first element was removed)
            middle_pos = (total_len - 1) // 2
            
            if middle_pos < len(first_half):
                # Middle is in first_half
                first_half.pop()
                # Rebalance by moving an item from second_half to first_half
                if second_half:
                    first_half.append(second_half.popleft())
            else:
                # Middle is in second_half
                second_half.popleft()
        
        # Rebalance the deques to maintain the "middle" at the boundary
        while len(first_half) + 1 < len(second_half):
            first_half.append(second_half.popleft())
        
        current_shot = (current_shot + 1) % 3
    
    print(shot_count)

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")