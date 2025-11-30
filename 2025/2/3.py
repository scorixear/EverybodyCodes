import os, sys
import time

class Complex:
    def __init__(self, real=0, imag=0):
        self.real = real
        self.imag = imag
    def __add__(self, other):
        return Complex(self.real + other.real, self.imag + other.imag)
    def __mul__(self, other):
        return Complex(self.real * other.real - self.imag * other.imag, self.real * other.imag + self.imag * other.real)
    def __floordiv__(self, other):
        return Complex(int(self.real / other.real), int(self.imag / other.imag))
    def __str__(self):
        return f"[{self.real},{self.imag}]"
    def __repr__(self):
        return f"[{self.real},{self.imag}]"
    def copy(self):
        return Complex(self.real, self.imag)

def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    a_str = lines[0][2:].split(',')
    A = Complex(int(a_str[0][1:]), int(a_str[1][:-1]))
    grid_size = 1001
    step = 1000 // (grid_size - 1)
    
    grid = []
    engraved_points = 0
    max_val = 1000000
    min_val = -1000000
    for y in range(grid_size):
        row = []
        for x in range(grid_size):
            R = Complex()
            P = Complex(A.real + x * step, A.imag + y * step)
            exceeded = False
            
            for _ in range(100):
                R = R * R
                R = R // Complex(100000, 100000)
                R = R + P
                if R.real > max_val or R.real < min_val or R.imag > max_val or R.imag < min_val:
                    row.append(' ')
                    exceeded = True
                    break
            if not exceeded:
                row.append('#')
                engraved_points += 1
        grid.append(row)
    with open(os.path.join(sys.path[0],"o3.txt"), "w", encoding="utf-8") as f:
        for row in grid:
            f.write(''.join(row) + '\n')
    print(f"Engraved points: {engraved_points}")
                
    
    


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
