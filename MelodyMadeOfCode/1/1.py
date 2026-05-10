import os, sys
import time


class Scale:
    def __init__(self, identifier: int, colors: list[str]):
        self.identifier = identifier
        red = colors[0]
        green = colors[1]
        blue = colors[2]
        self.red = self.get_color(red, "r", "R")
        self.green = self.get_color(green, "g", "G")
        self.blue = self.get_color(blue, "b", "B")

    def get_color(self, color: str, lower: str, upper: str) -> int:
        result = 0
        for i, char in enumerate(color[::-1]):
            if char == upper:
                result += 2**i
        return result


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    scales: list[Scale] = []
    for line in lines:
        identifier, colors = line.split(":")
        colors = colors.split(" ")
        scales.append(Scale(int(identifier), colors))
    result = 0
    for scale in scales:
        if scale.green > scale.red and scale.green > scale.blue:
            result += scale.identifier
    print(result)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
