from numberlink import HexLink
from algorithms import solve
import itertools
import argparse
import sys


class ConsoleHexLink:
    LEFT_SYMBOL = " \\"
    RIGHT_SYMBOL = "/ "

    def __init__(self, field, solutions_amount=None):
        if solutions_amount is not None and solutions_amount < 0:
            raise ValueError("Количество решений должно быть неотрицательным.")
        self.game = HexLink(field)
        self.amount = solutions_amount

    def show_solutions(self):
        solutions = solve(self.game)
        founded = False
        for i, solution in enumerate(solutions):
            founded = True
            if self.amount is not None and i + 1 > self.amount:
                break
            print(self._get_solution_string(solution))
        if not founded:
            print("Решений нет.")

    def _get_solution_string(self, solution):
        solution = {frozenset(pair) for pair in solution}

        horizontal = self._get_horizontal_part(solution)
        vertical = self._get_vertical_part(solution)

        # Попеременно совмещаем строки
        merged = itertools.chain(
            *itertools.zip_longest(horizontal, vertical, fillvalue="")
        )
        return "\n".join(merged)

    def _get_horizontal_part(self, solution):
        result = []
        intend = self.game.size - 1

        for i, level in enumerate(self.game.field):
            current = " " * abs(intend)
            for j, cell in enumerate(level):
                condition = frozenset(((i, j), (i, j + 1))) in solution
                between = "--" if condition else "  "
                current += f"{str(cell)} {between} "
            result.append(current.rstrip())
            intend -= 2

        return result

    def _get_vertical_part(self, solution):
        result = []
        intend = self.game.size

        for i, level in enumerate(self.game.field):
            current = " " * (abs(intend) - 1)
            for j in range(len(level) + 1):
                left = self._get_left((i, j), solution)
                right = self._get_right((i, j), solution)
                line = f"{left} {right}"
                current += line
            result.append(current.rstrip())
            intend -= 2

        return result[1:]

    def _get_left(self, start, solution):
        return self._get_edge(start, ConsoleHexLink.LEFT_SYMBOL, solution)

    def _get_right(self, start, solution):
        return self._get_edge(start, ConsoleHexLink.RIGHT_SYMBOL, solution)

    def _get_edge(self, start, symbol, solution):
        i, j = start
        ends = {
            ConsoleHexLink.LEFT_SYMBOL: ((i - 1, j - 1), (i - 1, j)),
            ConsoleHexLink.RIGHT_SYMBOL: ((i - 1, j), (i - 1, j + 1)),
        }
        end = ends[symbol][0] if i <= self.game.size // 2 else ends[symbol][1]
        condition = frozenset((start, end)) in solution
        empty = "  " if self.game.is_valid(*end) else ""
        return symbol if condition else empty


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number",
                        help="the number of solutions to print",
                        nargs='?',
                        type=int,
                        action="store")
    parser.add_argument("-g", "--generate",
                        help="generate instance of Numberlink",
                        action="store_true")
    return parser


def enter_field():
    field = []
    while line := input().split():
        field.append(line)
    return field


def main():
    args = create_parser().parse_args()
    field = None
    if args.generate:
        ...
        # field = generator.create_field()
    else:
        field = enter_field()
    try:
        game = ConsoleHexLink(field, args.number)
        game.show_solutions()
    except ValueError as err:
        print(err.args[0])
        sys.exit(-1)


if __name__ == "__main__":
    main()
