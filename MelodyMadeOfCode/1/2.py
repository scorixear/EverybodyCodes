import os, sys
import time


class Scale:
    def __init__(self, identifier: int, colors: list[str]):
        self.identifier = identifier
        self.red = self.get_color(colors[0], "r", "R")
        self.green = self.get_color(colors[1], "g", "G")
        self.blue = self.get_color(colors[2], "b", "B")
        self.shine = self.get_color(colors[3], "s", "S")

    def get_color(self, color: str, lower: str, upper: str) -> int:
        result = 0
        for i, char in enumerate(color[::-1]):
            if char == upper:
                result += 2**i
        return result


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    scales: list[Scale] = []
    for line in lines:
        identifier, colors = line.split(":")
        colors = colors.split(" ")
        scales.append(Scale(int(identifier), colors))
    scales.sort(key=lambda x: x.shine, reverse=True)
    max_shine = scales[0].shine
    darkest_colors = 255 * 3
    darkest_id = 0
    for scale in scales:
        if scale.shine < max_shine:
            break
        if scale.red + scale.green + scale.blue < darkest_colors:
            darkest_id = scale.identifier
            darkest_colors = scale.red + scale.green + scale.blue
    print(darkest_id)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
