import collections
import itertools
from graph_tools import Graph

CELL_EMPTY = 0
MAX_NUMBER = 100


class HexagonalField:
    def __init__(self, field):
        self._check_hexagonal(field)
        self.field = [list(map(int, level)) for level in field]

    def __setitem__(self, key, value):
        level, index = key
        self.field[level][index] = value

    def __getitem__(self, key):
        level, index = key
        return self.field[level][index]

    def get_environment(self, level, index):
        directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]

        if level < self.size // 2:
            directions.extend([(-1, -1), (1, 1)])
        elif level > self.size // 2:
            directions.extend([(-1, 1), (1, -1)])
        else:
            directions.extend([(-1, -1), (1, -1)])

        for dy, dx in directions:
            yield level + dy, index + dx

    def get_neighbours(self, level, index):
        yield from (position for position in self.get_environment(level, index)
                    if self.is_valid(*position))

    @staticmethod
    def _check_hexagonal(field):
        size = {
            "vertical": len(field),
            "horizontal": max(len(level) for level in field)
        }
        if size["vertical"] != size["horizontal"] or size["vertical"] % 2 == 0:
            raise ValueError(
                f"Некорректные размеры поля: "
                f"{size['horizontal']} x {size['vertical']}")
        middle = len(field) // 2
        for i in range(middle):
            if len(field[middle - i - 1]) != len(field) - i - 1:
                raise ValueError(f"Неверная длина {i - 1}-го уровня.")
            if len(field[middle + i + 1]) != len(field) - i - 1:
                raise ValueError(f"Неверная длина {i + 1}-го уровня.")

    @property
    def size(self):
        return len(self.field)

    def is_valid(self, level, key):
        return (0 <= level < len(self.field)
                and 0 <= key < len(self.field[level]))

    def make_graph(self):
        """
        Строит граф шестиугольного поля и возвращает его.
        """
        graph = Graph(directed=False, multiedged=False)

        middle = len(self.field) // 2
        for i, level in enumerate(self.field):
            for j, cell, in enumerate(level):
                start = i, j
                ends = {
                    (i + 1, j),
                    (i, j + 1),
                    (i + 1, j + 1) if i < middle else (i + 1, j - 1)
                }

                for valid_end in (end for end in ends if self.is_valid(*end)):
                    graph.add_edge(start, valid_end)

        return graph


class HexLink(HexagonalField):

    def __init__(self, field):
        HexLink._check_field(field)
        super().__init__(field)

    def __getitem__(self, key):
        level, index = key
        return self.field[level][index]

    def __setitem__(self, key, value):
        level, index = key
        self.field[level][index] = value

    def get_targets(self):
        """
        Принимает на вход задачу Numberlink.
        Возвращает словарь с координатами всех непустых клеток, а также парами
        клеток, которые нужно соединить.
        """
        targets = {"vertices": set(), "pairs": set()}
        pairs = {}

        for i, level in enumerate(self.field):
            for j, cell in enumerate(level):
                if cell is not CELL_EMPTY:
                    if cell in pairs:
                        targets["pairs"].add(frozenset((pairs[cell], (i, j))))
                    else:
                        pairs[cell] = (i, j)
                    targets["vertices"].add((i, j))

        return targets

    @staticmethod
    def _check_field(field):
        if field is None:
            raise ValueError("Поле было None.")
        HexLink._check_cells(field)
        HexLink._check_pairs(field)
        HexLink._check_range(field)
        HexLink._check_order(field)

    @staticmethod
    def _check_pairs(field):
        items = collections.Counter(map(str, itertools.chain(*field)))
        del items[str(CELL_EMPTY)]
        if not items:
            raise ValueError("Не обнаружено пар чисел.")
        filtered = [number for number, repeat in items.items() if repeat != 2]
        if filtered:
            raise ValueError(
                f"Некорректное количество чисел: {', '.join(filtered)}"
            )

    @staticmethod
    def _check_range(field):
        for number in map(int, itertools.chain(*field)):
            if number > MAX_NUMBER:
                raise ValueError(
                    f"Числа не могут превышать: {MAX_NUMBER}."
                    f" Было получено: {number}"
                )
            if number < CELL_EMPTY:
                raise ValueError(
                    f"Числа не могут быть отрицательными."
                    f" Было получено: {number}"
                )

    @staticmethod
    def _check_order(field):
        items = {*map(int, itertools.chain(*field))}
        failed = [i for i in range(max(*items) + 1) if i not in items]
        if failed:
            raise ValueError(
                    f"Нарушен порядок следования. "
                    f"Не обнаружено: {', '.join(map(str, failed))}"
            )

    @staticmethod
    def _check_cells(field):
        for i, level in enumerate(field):
            for j, cell in enumerate(level):
                if not str(cell).isnumeric():
                    raise ValueError(f"Некорректный символ на позиции {i, j}")
