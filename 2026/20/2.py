import os, sys
import time
from enum import Enum
from numpy import base_repr


class Operator(Enum):
    PLUS = 2
    MINUS = 1

    def count(self):
        return self.value


class Equation:
    def __init__(self, line: str) -> None:
        seg1, seg2 = line.split(" = ")

        self.left: tuple[int, str, Operator, int, str] = self._parse(seg1)
        self.right: tuple[int, str, Operator, int, str] = self._parse(seg2)

    def _parse(self, seg: str):
        if seg.find("+") != -1:
            operator = Operator.PLUS
            left, right = [(x, from_base11(x)) for x in seg.split(" + ")]
        else:
            operator = Operator.MINUS
            left, right = [(x, from_base11(x)) for x in seg.split(" - ")]
        return (left[1], left[0], operator, right[1], right[0])

    def is_correct(self):
        left = self._calc(self.left)
        right = self._calc(self.right)
        return left == right

    def _calc(self, val: tuple[int, str, Operator, int, str]):
        initial = val[0]
        match val[2]:
            case Operator.PLUS:
                initial += val[3]
            case Operator.MINUS:
                initial -= val[3]
        return initial

    def count_segments(self):
        left = self._count(self.left)
        right = self._count(self.right)
        return left + 2 + right

    def _count(self, val: tuple[int, str, Operator, int, str]):
        return self._count_val(val[1]) + val[2].count() + self._count_val(val[4])

    def _count_val(self, val: str):
        total = 0
        for c in val:
            match c:
                case "0":
                    total += 6
                case "1":
                    total += 2
                case "2":
                    total += 5
                case "3":
                    total += 5
                case "4":
                    total += 4
                case "5":
                    total += 5
                case "6":
                    total += 6
                case "7":
                    total += 3
                case "8":
                    total += 7
                case "9":
                    total += 6
                case "A":
                    total += 6
        return total


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    total = 0
    for line in lines:
        equation = Equation(line)
        if equation.is_correct():
            total += equation.count_segments()
    print(to_base11(total))


def to_base11(val: int):
    return base_repr(val, 11)


def from_base11(val: str):
    return int(val, base=11)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
