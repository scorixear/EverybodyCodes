import os, sys
import time
class Complex:
    def __init__(self, real=0, imag=0):
        self.real = real
        self.imag = imag
    def __add__(self, other):
        return Complex(self.real + other.real, self.imag + other.imag)
    def __sub__(self, other):
        return Complex(self.real - other.real, self.imag - other.imag)
    def __mul__(self, other):
        return Complex(self.real * other.real - self.imag * other.imag, self.real * other.imag + self.imag * other.real)
    def __floordiv__(self, other):
        return Complex(self.real // other.real, self.imag // other.imag)
    def __str__(self):
        return f"[{self.real},{self.imag}]"
    def __repr__(self):
        return f"[{self.real},{self.imag}]"

def main():
    with open(os.path.join(sys.path[0],"i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    a_str = lines[0][2:].split(',')
    A = Complex(int(a_str[0][1:]), int(a_str[1][:-1]))
    
    R = Complex()
    
    for _ in range(3):
        R = R * R
        R = R // Complex(10, 10)
        R = R + A
    print(R)
    


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
