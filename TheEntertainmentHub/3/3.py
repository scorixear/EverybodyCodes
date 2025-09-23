import os, sys
import time
class Dice:
    def __init__(self, dice_id: int, faces: list[int], seed: int):
        self.pulse = seed
        self.seed = seed
        self.faces = faces
        self.id = dice_id
        self.face_id = 0
        self.roll_number = 1
        self.spin = 0
        self.target = 0
        self.rolls = []
        self.current_roll = 0
    def roll(self) -> int:
        self.spin = self.roll_number * self.pulse
        self.face_id = (self.face_id + self.spin) % len(self.faces)
        self.pulse += self.spin
        self.pulse %= self.seed
        self.pulse += 1 + self.roll_number + self.seed
        self.roll_number += 1
        return self.faces[self.face_id]
    def next_target(self, sequence: list[int]) -> bool:
        if self.target >= len(sequence) - 1:
            return True
        self.target += 1
        return False
    def precompute(self, cell_count: int):
        self.rolls = []
        self.current_roll = 0
        for _ in range(cell_count):
            self.rolls.append(self.roll())
    def next(self, step: int ) -> int:
        val = self.rolls[step]
        return val

def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    dices: list[Dice] = []
    grid: list[list[int]] = []
    read_dice = True
    for line in lines:
        if line == "":
            read_dice = False
            continue
        if read_dice:
            parts = line.split(" ")
            dice_id = int(parts[0][:-1])
            faces = list(map(int, parts[1].split("=")[1][1:-1].split(",")))
            seed = int(parts[2].split("=")[1])
            dices.append(Dice(dice_id, faces, seed))
        else:
            grid.append(list(map(int, line)))
    
    cell_count = len(grid) * len(grid[0])
    total_visited = set()
    for dice in dices:
        dice.precompute(cell_count + 10_000)
        val = dice.next(0)
        stack = [(x, y, 0, True) for x in range(len(grid[0])) for y in range(len(grid)) if grid[y][x] == val]
        total_visited |= explore(grid, dice, stack)
    print_grid(grid, total_visited)
    print(len(total_visited))
  
def explore(grid: list[list[int]], dice: Dice, start_positions: list[tuple[int, int, int, bool]]):
    total_visited = set()
    for pos in start_positions:
        stack = [pos]
        visited = set()
        while stack:
            x, y, step, moved = stack.pop()
            if (x, y, step) in visited and moved:
                continue
            visited.add((x, y, step))
            dxy = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            next_val = dice.next(step+1)
            for dx, dy in dxy:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                    if grid[ny][nx] == next_val:
                        stack.append((nx, ny, step + 1, True))
            if grid[y][x] == next_val:
                stack.append((x, y, step + 1, False))
        for x, y, _ in visited:
            total_visited.add((x, y))
    return total_visited

def print_grid(grid: list[list[int]], visited: set[tuple[int, int]]):
    with open(os.path.join(sys.path[0],"o3.txt"), "w", encoding="utf-8") as f:
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if (x, y) in visited:
                    f.write(str(grid[y][x]))
                else:
                    f.write(" ")
            f.write("\n")

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
