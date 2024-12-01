import os, sys
import time

class Block:
    def __init__(self, top_x, top_y, grid: list[list[str]]):
        self.min_x = top_x+2
        self.min_y = top_y+2
        self.max_x = top_x+6
        self.max_y = top_y+6
        self.original = [[grid[j][i] for i in range(self.min_x, self.max_x)] for j in range(self.min_y, self.max_y)]
        self.solved = False
    
    def get_hints(self, grid: list[list[str]], x: int, y: int):
        return [[grid[y][self.min_x - 2], grid[y][self.min_x - 1], grid[y][self.max_x], grid[y][self.max_x + 1]],
                [grid[self.min_y - 2][x], grid[self.min_y - 1][x], grid[self.max_y][x], grid[self.max_y + 1][x]]]
    def get_matching_hint(self, row_hints: list[str], col_hints: list[str]):
        candidates = []
        for row in row_hints:
            if row in col_hints and row != "?":
                candidates.append(row)
        if len(candidates) == 1:
            return candidates[0]
        return None
    
    def first_pass(self, grid: list[list[str]]):
        self.solved = True
        for y in range(self.min_y, self.max_y):
            for x in range(self.min_x, self.max_x):
                [rowhints, colhints] = self.get_hints(grid, x, y)
                matching = self.get_matching_hint(rowhints, colhints)
                if matching:
                    grid[y][x] = matching
                else:
                    self.solved = False
    def find_missing_pair(self, grid: list[list[str]], row_hints: list[str], col_hints: list[str], x: int, y: int):
        row_symbols = [grid[y][i] for i in range(self.min_x, self.max_x)]
        col_symbols = [grid[i][x] for i in range(self.min_y, self.max_y)]
        solutions = []
        for hint in row_hints:
            if hint not in row_symbols and hint != "?":
                solutions.append(hint)
        for hint in col_hints:
            if hint not in col_symbols and hint != "?":
                solutions.append(hint)
        return solutions
                
    def find_question_marks(self, grid: list[list[str]], x: int, y: int):
        questionmarks = []
        if grid[self.min_y - 2][x] == "?":
            questionmarks.append((self.min_y - 2, x))
        if grid[self.min_y - 1][x] == "?":
            questionmarks.append((self.min_y - 1, x))
        if grid[self.max_y][x] == "?":
            questionmarks.append((self.max_y, x))
        if grid[self.max_y + 1][x] == "?":
            questionmarks.append((self.max_y + 1, x))
        if grid[y][self.min_x - 2] == "?":
            questionmarks.append((y, self.min_x - 2))
        if grid[y][self.min_x - 1] == "?":
            questionmarks.append((y, self.min_x - 1))
        if grid[y][self.max_x] == "?":
            questionmarks.append((y, self.max_x))
        if grid[y][self.max_x + 1] == "?":
            questionmarks.append((y, self.max_x + 1))
        return questionmarks
    
    def second_pass(self, grid: list[list[str]]):
        found_match = True
        affected = []
        while found_match:
            found_match = False
            for y in range(self.min_y, self.max_y):
                for x in range(self.min_x, self.max_x):
                    if grid[y][x] == ".":
                        question_marks = self.find_question_marks(grid, x, y)
                        if len(question_marks) == 1:
                            [rowhints, colhints] = self.get_hints(grid, x, y)
                            missing_pair = self.find_missing_pair(grid, rowhints, colhints, x, y)
                            if len(missing_pair) == 1:
                                grid[y][x] = missing_pair[0]
                                grid[question_marks[0][0]][question_marks[0][1]] = missing_pair[0]
                                affected.append(question_marks[0])
                                found_match = True
        self.solved = True
        for y in range(self.min_y, self.max_y):
            for x in range(self.min_x, self.max_x):
                if grid[y][x] == ".":
                    self.solved = False
        return affected
    
    def should_reconsider(self, x: int, y: int):
        if self.solved:
            return False
        if self.min_x - 2 <= x <= self.max_x + 1 and self.min_y - 2 <= y <= self.max_y + 1:
            return True
        return False
        
    def __str__(self):
        return "\n".join(["".join(row) for row in self.original])
    def __repr__(self):
        return self.__str__()
    def print(self, grid: list[list[str]]):
        if self.solved:
            return ["".join([grid[j][i] for i in range(self.min_x, self.max_x)]) for j in range(self.min_y, self.max_y)]
        return ["".join(row) for row in self.original]

def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    grid = [list(line) for line in lines]
    
    original_blocks = []
    blocks: list[Block] = []
    for row in range(0, len(grid) - 6, 6):
        for col in range(0, len(grid[0]) - 6, 6):
            block = Block(col, row, grid)
            blocks.append(block)
            original_blocks.append(block)

    for i in range(2):
        while blocks:
            block = blocks.pop()
            block.first_pass(grid)
            affected = block.second_pass(grid)
            for x, y in affected:
                if block.should_reconsider(x, y) and block not in blocks:
                    blocks.append(block)
        blocks = original_blocks.copy()
    
                
    total = 0
    
    for row in range(0, len(grid)-2, 6):
        for col in range(0, len(grid[row])-2, 6):
            is_done = check_is_done(row, col, grid)
            if is_done:
                word = []
                for i in range(row+2, row+6):
                    for j in range(col+2, col+6):
                        word.append(grid[i][j])
                base_power = [ord(symbol) - 64 for symbol in word]
                powers = [p * i for i, p in enumerate(base_power, 1)]
                total += sum(powers)
    print(total)
def check_is_done(row: int, col: int, grid: list[list[str]]):
    for i in range(row + 2, row + 6):
        for j in range(col + 2, col + 6):
            if grid[i][j] == ".":
                return False
    return True

    
if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
