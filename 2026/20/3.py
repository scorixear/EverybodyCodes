import os, sys
import time
from enum import Enum
from numpy import base_repr


class Operator(Enum):
    PLUS = 2
    MINUS = 1

    def count(self):
        return self.value

    def can_produce(self) -> list["Operator"]:
        if self == Operator.PLUS:
            return [Operator.MINUS]
        return []

    def can_receive(self) -> list["Operator"]:
        if self == Operator.MINUS:
            return [Operator.PLUS]
        return []

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        if self == Operator.PLUS:
            return "+"
        return "-"


class Value:
    def __init__(self, val: str):
        self.str_val = val
        self.val = from_base11(val)

    def count(self):
        total = 0
        for c in self.str_val:
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

    def can_produce(self) -> list["Value"]:
        producable = []
        for i, c in enumerate(self.str_val):
            match c:
                # cannot remove: 0, 1, 2, 3, 4, 5
                case "6":
                    producable.append(
                        Value(self.str_val[:i] + "5" + self.str_val[i + 1 :])
                    )
                case "7":
                    producable.append(
                        Value(self.str_val[:i] + "1" + self.str_val[i + 1 :])
                    )
                case "8":
                    producable.append(
                        Value(self.str_val[:i] + "0" + self.str_val[i + 1 :])
                    )
                    producable.append(
                        Value(self.str_val[:i] + "9" + self.str_val[i + 1 :])
                    )
                    producable.append(
                        Value(self.str_val[:i] + "6" + self.str_val[i + 1 :])
                    )
                    producable.append(
                        Value(self.str_val[:i] + "A" + self.str_val[i + 1 :])
                    )
                case "9":
                    producable.append(
                        Value(self.str_val[:i] + "3" + self.str_val[i + 1 :])
                    )
                    producable.append(
                        Value(self.str_val[:i] + "5" + self.str_val[i + 1 :])
                    )
        return producable

    def can_receive(self) -> list["Value"]:
        receivable = []
        for i, c in enumerate(self.str_val):
            match c:
                # cannot receive: 2, 4, 7, 8
                case "0":
                    receivable.append(
                        Value(self.str_val[:i] + "8" + self.str_val[i + 1 :])
                    )
                case "1":
                    receivable.append(
                        Value(self.str_val[:i] + "7" + self.str_val[i + 1 :])
                    )
                case "3":
                    receivable.append(
                        Value(self.str_val[:i] + "9" + self.str_val[i + 1 :])
                    )
                case "5":
                    receivable.append(
                        Value(self.str_val[:i] + "6" + self.str_val[i + 1 :])
                    )
                    receivable.append(
                        Value(self.str_val[:i] + "9" + self.str_val[i + 1 :])
                    )
                case "6":
                    receivable.append(
                        Value(self.str_val[:i] + "8" + self.str_val[i + 1 :])
                    )
                case "9":
                    receivable.append(
                        Value(self.str_val[:i] + "8" + self.str_val[i + 1 :])
                    )
                case "A":
                    receivable.append(
                        Value(self.str_val[:i] + "8" + self.str_val[i + 1 :])
                    )
        return receivable

    def can_move(self) -> list["Value"]:
        movable = []
        for i, c in enumerate(self.str_val):
            match c:
                # cannot move: 1, 4, 7, 8
                case "0":
                    movable.append(
                        Value(self.str_val[:i] + "A" + self.str_val[i + 1 :])
                    )
                    movable.append(
                        Value(self.str_val[:i] + "9" + self.str_val[i + 1 :])
                    )
                    movable.append(
                        Value(self.str_val[:i] + "6" + self.str_val[i + 1 :])
                    )
                case "2":
                    movable.append(
                        Value(self.str_val[:i] + "3" + self.str_val[i + 1 :])
                    )
                case "3":
                    movable.append(
                        Value(self.str_val[:i] + "2" + self.str_val[i + 1 :])
                    )
                    movable.append(
                        Value(self.str_val[:i] + "5" + self.str_val[i + 1 :])
                    )
                case "5":
                    movable.append(
                        Value(self.str_val[:i] + "3" + self.str_val[i + 1 :])
                    )
                case "6":
                    movable.append(
                        Value(self.str_val[:i] + "A" + self.str_val[i + 1 :])
                    )
                    movable.append(
                        Value(self.str_val[:i] + "9" + self.str_val[i + 1 :])
                    )
                    movable.append(
                        Value(self.str_val[:i] + "0" + self.str_val[i + 1 :])
                    )
                case "9":
                    movable.append(
                        Value(self.str_val[:i] + "A" + self.str_val[i + 1 :])
                    )
                    movable.append(
                        Value(self.str_val[:i] + "6" + self.str_val[i + 1 :])
                    )
                    movable.append(
                        Value(self.str_val[:i] + "0" + self.str_val[i + 1 :])
                    )
                case "A":
                    movable.append(
                        Value(self.str_val[:i] + "9" + self.str_val[i + 1 :])
                    )
                    movable.append(
                        Value(self.str_val[:i] + "6" + self.str_val[i + 1 :])
                    )
                    movable.append(
                        Value(self.str_val[:i] + "0" + self.str_val[i + 1 :])
                    )
        return movable

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.str_val


class Equation:
    def __init__(self, line: str) -> None:
        seg1, seg2 = line.split(" = ")

        self.left: tuple[Value, Operator, Value] = self._parse(seg1)
        self.right: tuple[Value, Operator, Value] = self._parse(seg2)

    def _parse(self, seg: str):
        if seg.find("+") != -1:
            operator = Operator.PLUS
            left, right = [Value(x) for x in seg.split(" + ")]
        else:
            operator = Operator.MINUS
            left, right = [Value(x) for x in seg.split(" - ")]
        return (left, operator, right)

    def is_correct(self):
        left = self._calc(self.left)
        right = self._calc(self.right)
        return left == right

    def _calc(self, val: tuple[Value, Operator, Value]):
        initial = val[0].val
        match val[1]:
            case Operator.PLUS:
                initial += val[2].val
            case Operator.MINUS:
                initial -= val[2].val
        return initial

    def count_segments(self):
        left = self._count(self.left)
        right = self._count(self.right)
        return left + 2 + right

    def _count(self, val: tuple[Value, Operator, Value]):
        return val[0].count() + val[1].count() + val[2].count()

    def try_different(self):
        left_left_receivable = self.left[0].can_receive()
        left_op_receivable = self.left[1].can_receive()
        left_right_receivable = self.left[2].can_receive()
        right_left_receivable = self.right[0].can_receive()
        right_op_receivable = self.right[1].can_receive()
        right_right_receivable = self.right[2].can_receive()

        # try each movable
        for val in self.left[0].can_move():
            tmp = self.left
            self.left = (val, self.left[1], self.left[2])
            if self.is_correct():
                return True
            self.left = tmp
        for val in self.left[2].can_move():
            tmp = self.left
            self.left = (self.left[0], self.left[1], val)
            if self.is_correct():
                return True
            self.left = tmp
        for val in self.right[0].can_move():
            tmp = self.right
            self.right = (val, self.right[1], self.right[2])
            if self.is_correct():
                return True
            self.right = tmp
        for val in self.right[2].can_move():
            tmp = self.right
            self.right = (self.right[0], self.right[1], val)
            if self.is_correct():
                return True
            self.right = tmp

        # try each producer
        for val in self.left[0].can_produce():
            tmp1 = self.left
            self.left = (val, self.left[1], self.left[2])
            # try each receiver
            for rec in self.left[0].can_receive():
                tmp2 = self.left
                self.left = (rec, self.left[1], self.left[2])
                if self.is_correct():
                    return True
                self.left = tmp2
            for rec in left_op_receivable:
                tmp2 = self.left
                self.left = (self.left[0], rec, self.left[2])
                if self.is_correct():
                    return True
                self.left = tmp2
            for rec in left_right_receivable:
                tmp2 = self.left
                self.left = (self.left[0], self.left[1], rec)
                if self.is_correct():
                    return True
                self.left = tmp2
            for rec in right_left_receivable:
                tmp2 = self.right
                self.right = (rec, self.right[1], self.right[2])
                if self.is_correct():
                    return True
                self.right = tmp2
            for rec in right_op_receivable:
                tmp2 = self.right
                self.right = (self.right[0], rec, self.right[2])
                if self.is_correct():
                    return True
                self.right = tmp2
            for rec in right_right_receivable:
                tmp2 = self.right
                self.right = (self.right[0], self.right[1], rec)
                if self.is_correct():
                    return True
                self.right = tmp2

            self.left = tmp1

        for val in self.left[1].can_produce():
            tmp1 = self.left
            self.left = (self.left[0], val, self.left[2])
            # try each receiver
            for rec in left_left_receivable:
                tmp2 = self.left
                self.left = (rec, self.left[1], self.left[2])
                if self.is_correct():
                    return True
                self.left = tmp2
            for rec in left_right_receivable:
                tmp2 = self.left
                self.left = (self.left[0], self.left[1], rec)
                if self.is_correct():
                    return True
                self.left = tmp2
            for rec in right_left_receivable:
                tmp2 = self.right
                self.right = (rec, self.right[1], self.right[2])
                if self.is_correct():
                    return True
                self.right = tmp2
            for rec in right_op_receivable:
                tmp2 = self.right
                self.right = (self.right[0], rec, self.right[2])
                if self.is_correct():
                    return True
                self.right = tmp2
            for rec in right_right_receivable:
                tmp2 = self.right
                self.right = (self.right[0], self.right[1], rec)
                if self.is_correct():
                    return True
                self.right = tmp2

            self.left = tmp1

        for val in self.left[2].can_produce():
            tmp1 = self.left
            self.left = (self.left[0], self.left[1], val)
            # try each receiver
            for rec in left_left_receivable:
                tmp2 = self.left
                self.left = (rec, self.left[1], self.left[2])
                if self.is_correct():
                    return True
                self.left = tmp2
            for rec in left_op_receivable:
                tmp2 = self.left
                self.left = (self.left[0], rec, self.left[2])
                if self.is_correct():
                    return True
                self.left = tmp2
            for rec in self.left[2].can_receive():
                tmp2 = self.left
                self.left = (self.left[0], self.left[1], rec)
                if self.is_correct():
                    return True
                self.left = tmp2
            for rec in right_left_receivable:
                tmp2 = self.right
                self.right = (rec, self.right[1], self.right[2])
                if self.is_correct():
                    return True
                self.right = tmp2
            for rec in right_op_receivable:
                tmp2 = self.right
                self.right = (self.right[0], rec, self.right[2])
                if self.is_correct():
                    return True
                self.right = tmp2
            for rec in right_right_receivable:
                tmp2 = self.right
                self.right = (self.right[0], self.right[1], rec)
                if self.is_correct():
                    return True
                self.right = tmp2

            self.left = tmp1

        for val in self.right[0].can_produce():
            tmp1 = self.right
            self.right = (val, self.right[1], self.right[2])
            # try each receiver
            for rec in left_left_receivable:
                tmp2 = self.left
                self.left = (rec, self.left[1], self.left[2])
                if self.is_correct():
                    return True
                self.left = tmp2
            for rec in left_op_receivable:
                tmp2 = self.left
                self.left = (self.left[0], rec, self.left[2])
                if self.is_correct():
                    return True
                self.left = tmp2
            for rec in left_right_receivable:
                tmp2 = self.left
                self.left = (self.left[0], self.left[1], rec)
                if self.is_correct():
                    return True
                self.left = tmp2
            for rec in self.right[0].can_receive():
                tmp2 = self.right
                self.right = (rec, self.right[1], self.right[2])
                if self.is_correct():
                    return True
                self.right = tmp2
            for rec in right_op_receivable:
                tmp2 = self.right
                self.right = (self.right[0], rec, self.right[2])
                if self.is_correct():
                    return True
                self.right = tmp2
            for rec in right_right_receivable:
                tmp2 = self.right
                self.right = (self.right[0], self.right[1], rec)
                if self.is_correct():
                    return True
                self.right = tmp2

            self.right = tmp1

        for val in self.right[1].can_produce():
            tmp1 = self.right
            self.right = (self.right[0], val, self.right[2])
            # try each receiver
            for rec in left_left_receivable:
                tmp2 = self.left
                self.left = (rec, self.left[1], self.left[2])
                if self.is_correct():
                    return True
                self.left = tmp2
            for rec in left_op_receivable:
                tmp2 = self.left
                self.left = (self.left[0], rec, self.left[2])
                if self.is_correct():
                    return True
                self.left = tmp2
            for rec in left_right_receivable:
                tmp2 = self.left
                self.left = (self.left[0], self.left[1], rec)
                if self.is_correct():
                    return True
                self.left = tmp2
            for rec in right_left_receivable:
                tmp2 = self.right
                self.right = (rec, self.right[1], self.right[2])
                if self.is_correct():
                    return True
                self.right = tmp2
            for rec in right_right_receivable:
                tmp2 = self.right
                self.right = (self.right[0], self.right[1], rec)
                if self.is_correct():
                    return True
                self.right = tmp2

            self.right = tmp1

        for val in self.right[2].can_produce():
            tmp1 = self.right
            self.right = (self.right[0], self.right[1], val)
            # try each receiver
            for rec in left_left_receivable:
                tmp2 = self.left
                self.left = (rec, self.left[1], self.left[2])
                if self.is_correct():
                    return True
                self.left = tmp2
            for rec in left_op_receivable:
                tmp2 = self.left
                self.left = (self.left[0], rec, self.left[2])
                if self.is_correct():
                    return True
                self.left = tmp2
            for rec in left_right_receivable:
                tmp2 = self.left
                self.left = (self.left[0], self.left[1], rec)
                if self.is_correct():
                    return True
                self.left = tmp2
            for rec in right_left_receivable:
                tmp2 = self.right
                self.right = (rec, self.right[1], self.right[2])
                if self.is_correct():
                    return True
                self.right = tmp2
            for rec in right_op_receivable:
                tmp2 = self.right
                self.right = (self.right[0], rec, self.right[2])
                if self.is_correct():
                    return True
                self.right = tmp2
            for rec in self.right[2].can_receive():
                tmp2 = self.right
                self.right = (self.right[0], self.right[1], rec)
                if self.is_correct():
                    return True
                self.right = tmp2

            self.right = tmp1

        return False

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.left[0]} {self.left[1]} {self.left[2]} = {self.right[0]} {self.right[1]} {self.right[2]}"


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    total = 0
    for line in lines:
        equation = Equation(line)
        print(equation)
        if equation.is_correct():
            print("Correct")
            total += equation.count_segments()
        elif equation.try_different():
            print(equation)
            total += equation.count_segments()
        else:
            print("Wrong")
        print()
    print(to_base11(total))


def to_base11(val: int):
    return base_repr(val, 11)


def from_base11(val: str):
    return int(val, base=11)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
