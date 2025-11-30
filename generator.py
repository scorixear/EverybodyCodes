import os

python_code = """import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"e{0}.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\\n")

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {{time.perf_counter() - before:.6f}}s")
"""

YEAR = "2025"
for day in range(1, 21):
    if os.path.isdir(os.path.join(YEAR, str(day))):
        continue
    os.mkdir(os.path.join(YEAR, str(day)))
    with open(os.path.join(YEAR, str(day), "i1.txt"), "w", encoding="UTF-8") as f:
        pass
    with open(os.path.join(YEAR, str(day), "i2.txt"), "w", encoding="UTF-8") as f:
        pass
    with open(os.path.join(YEAR, str(day), "i3.txt"), "w", encoding="UTF-8") as f:
        pass
    with open(os.path.join(YEAR, str(day), "e1.txt"), "w", encoding="UTF-8") as f:
        pass
    with open(os.path.join(YEAR, str(day), "e2.txt"), "w", encoding="UTF-8") as f:
        pass
    with open(os.path.join(YEAR, str(day), "e3.txt"), "w", encoding="UTF-8") as f:
        pass
    with open(os.path.join(YEAR, str(day), "1.py"), "w", encoding="UTF-8") as f:
        f.write(python_code.format(1))
    with open(os.path.join(YEAR, str(day), "2.py"), "w", encoding="UTF-8") as f:
        f.write(python_code.format(2))
    with open(os.path.join(YEAR, str(day), "3.py"), "w", encoding="UTF-8") as f:
        f.write(python_code.format(3))
    