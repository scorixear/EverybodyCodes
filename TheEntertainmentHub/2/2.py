import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    balloons = list(map(lambda x: 0 if x == "R" else 1 if x == "G" else 2, lines[0])) * 100
    
    current_shot = 0
    shot_count = 0
    while balloons:
        shot_count += 1
        if balloons[0] == current_shot:
            if len(balloons)%2 == 0:
                balloons.pop(len(balloons)//2)
        balloons.pop(0)
        current_shot = (current_shot + 1) % 3
    print(shot_count)

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
