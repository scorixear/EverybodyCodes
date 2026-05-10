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

    def is_shiny(self) -> bool:
        return self.shine >= 33

    def is_matte(self) -> bool:
        return self.shine <= 30

    def is_dominant_red(self) -> bool:
        return self.red > self.green and self.red > self.blue

    def is_dominant_green(self) -> bool:
        return self.green > self.red and self.green > self.blue

    def is_dominant_blue(self) -> bool:
        return self.blue > self.red and self.blue > self.green


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    scales: list[Scale] = []
    for line in lines:
        identifier, colors = line.split(":")
        colors = colors.split(" ")
        scales.append(Scale(int(identifier), colors))
    groups = [
        [],  # red matte
        [],  # red shiny
        [],  # green matte
        [],  # green shiny
        [],  # blue matte
        [],  # blue shiny
    ]
    for scale in scales:
        if scale.is_shiny():
            if scale.is_dominant_red():
                groups[1].append(scale)
            elif scale.is_dominant_green():
                groups[3].append(scale)
            elif scale.is_dominant_blue():
                groups[5].append(scale)
        elif scale.is_matte():
            if scale.is_dominant_red():
                groups[0].append(scale)
            elif scale.is_dominant_green():
                groups[2].append(scale)
            elif scale.is_dominant_blue():
                groups[4].append(scale)
    groups.sort(key=lambda x: len(x), reverse=True)
    largest_group = groups[0]
    print(sum(scale.identifier for scale in largest_group))


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
