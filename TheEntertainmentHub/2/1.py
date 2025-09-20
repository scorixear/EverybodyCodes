import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    balloons = []
    recent_color = -1
    for c in lines[0]:
        color = 0 if c == "R" else 1 if c == "G" else 2
        if recent_color != color:
            balloons.append((color, 1))
            recent_color = color
        else:
            balloons[-1] = (color, balloons[-1][1] + 1)

    current_shot = 0
    shot_count = 0
    while balloons:
        shot_count += 1
        if balloons[0][0] == current_shot:
            balloons.pop(0)
            if not balloons:
                break
        if balloons[0][1] == 1:
            balloons.pop(0)
        else:
            balloons[0] = (balloons[0][0], balloons[0][1] - 1)
        current_shot = (current_shot + 1) % 3
        # print_balloons(balloons)
    print(shot_count)
def print_balloons(balloons):
    for color, count in balloons:
        c = "R" if color == 0 else "G" if color == 1 else "B"
        print(c*count, end="")
    print()

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
