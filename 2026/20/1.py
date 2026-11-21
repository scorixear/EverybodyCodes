import os, sys
import time
from enum import Enum


class Operator(Enum):
    PLUS = 2
    MINUS = 1

    def count(self):
        return self.value


class Equation:
    def __init__(self, line: str) -> None:
        seg1, seg2 = line.split(" = ")

        self.left: tuple[int, Operator, int] = self._parse(seg1)
        self.right: tuple[int, Operator, int] = self._parse(seg2)

    def _parse(self, seg: str):
        if seg.find("+") != -1:
            operator = Operator.PLUS
            left, right = [int(x) for x in seg.split(" + ")]
        else:
            operator = Operator.MINUS
            left, right = [int(x) for x in seg.split(" - ")]
        return (left, operator, right)

    def is_correct(self):
        left = self._calc(self.left)
        right = self._calc(self.right)
        return left == right

    def _calc(self, val: tuple[int, Operator, int]):
        initial = val[0]
        match val[1]:
            case Operator.PLUS:
                initial += val[2]
            case Operator.MINUS:
                initial -= val[2]
        return initial

    def count_segments(self):
        left = self._count(self.left)
        right = self._count(self.right)
        return left + 2 + right

    def _count(self, val: tuple[int, Operator, int]):
        return self._count_val(val[0]) + val[1].count() + self._count_val(val[2])

    def _count_val(self, val: int):
        match val:
            case 0:
                return 6
            case 1:
                return 2
            case 2:
                return 5
            case 3:
                return 5
            case 4:
                return 4
            case 5:
                return 5
            case 6:
                return 6
            case 7:
                return 3
            case 8:
                return 7
            case 9:
                return 6
        return 0


def main():
    with open(os.path.join(sys.path[0], "i1.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    total = 0
    for line in lines:
        equation = Equation(line)
        if equation.is_correct():
            total += equation.count_segments()
    print(total)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
