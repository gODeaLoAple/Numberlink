import collections
import itertools
from graph_tools import Graph


class Numberlink:
    CELL_EMPTY = 0
    """
    Интерфейс игры Numberlink.
    """
    def get_targets(self):
        raise NotImplementedError

    def make_graph(self):
        raise NotImplementedError


class HexLink(Numberlink):
    CELL_EMPTY = 0
    MAX_NUMBER = 9

    def __init__(self, field):
        HexLink.check_field(field)
        self.field = [list(map(int, level)) for level in field]

    def __getitem__(self, key):
        level, index = key
        return self.field[level][index]

    def __setitem__(self, key, value):
        level, index = key
        self.field[level][index] = value

    def is_valid(self, level, key):
        return (level in range(len(self.field))
                and key in range(len(self.field[level])))

    @property
    def size(self):
        return len(self.field)

    @staticmethod
    def check_field(field):
        if field is None:
            raise ValueError("Поле было None.")
        HexLink._check_hexagonal(field)
        HexLink._check_cells(field)
        HexLink._check_pairs(field)
        HexLink._check_range(field)
        HexLink._check_order(field)

    @staticmethod
    def _check_pairs(field):
        items = collections.Counter(map(str, itertools.chain(*field)))
        del items[str(Numberlink.CELL_EMPTY)]
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
            if number > HexLink.MAX_NUMBER:
                raise ValueError(
                    f"Числа не могут превышать: {HexLink.MAX_NUMBER}."
                    f" Было получено: {number}"
                )
            if number < HexLink.CELL_EMPTY:
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
                if cell is not Numberlink.CELL_EMPTY:
                    if cell in pairs:
                        targets["pairs"].add(frozenset((pairs[cell], (i, j))))
                    else:
                        pairs[cell] = (i, j)
                    targets["vertices"].add((i, j))

        return targets

    def make_graph(self):
        """
        Строит граф задачи Numberlink и возвращает его.
        В узлах находятся клетки игры, ребра - возможные переходы
        между клетками.
        Если на клете стоит цифра, то она находится в весе
        соответсвтующего узла.
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
