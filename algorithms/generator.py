import random
import itertools
from numberlink import HexagonalField, MAX_NUMBER, CELL_EMPTY


MAX_SIZE = 5
MIN_SIZE = 3


class Path:
    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end


class PathConstructor:
    def __init__(self, field):
        self.field = field
        self.covered_cells = 0
        self.cells_amount = centered_hex_number((self.field.size + 1) // 2)
        self.paths = []

    @property
    def number(self):
        return len(self.paths) + 1

    def count_added_neighbours_or_non_valid(self, position):
        return count(
            x for x in self.field.get_environment(*position)
            if not self.field.is_valid(*x) or self.field[x] != CELL_EMPTY
        )

    def count_numbered_neighbours(self, position, number):
        return count(
            x for x in self.field.get_neighbours(*position)
            if self.field[x] == number
        )

    def is_cycle(self, position, number):
        return self.count_numbered_neighbours(position, number) > 1

    def is_isolated(self, position, number, is_last):
        surround = 6
        return (
                self.count_added_neighbours_or_non_valid(position) == surround
                and (not is_last or self.is_cycle(position, number))
        )

    def has_isolated_empty_cells(self, position, number, is_last):
        """
        Проверка, есть ли среди пустых соседних клеток изолированная.
        """
        neighbours = self.field.get_neighbours(*position)
        return any(
            self.is_isolated(place, number, is_last) for place in neighbours
            if self.field[place] == CELL_EMPTY
        )

    def can_add_cell(self, position, number):
        self.field[position] = number
        isolated = self.has_isolated_empty_cells(position, number, True)
        self.field[position] = CELL_EMPTY
        return not isolated

    def get_path_extension_neighbour(self, position, number):
        """
        Производит поиск пустой соседней клетки, добавление которой в путь
        не создает изолированных точек.
        :param position:
        :param number:
        :return:
        """
        neighbours = list(self.field.get_neighbours(*position))
        start = random.randint(0, len(neighbours) - 1)
        if not self.has_isolated_empty_cells(position, number, False):
            for pos in neighbours[start:] + neighbours[:start]:
                if self.field[pos] == CELL_EMPTY:
                    if self.can_add_cell(pos, number):
                        return pos
        return None

    def try_get_new_path_begin(self):
        """
        Пытается найти пару пустых соседних клеток, добавление которых в
        новый путь не создаёт изолированных точек.
        В случае успеха возвращает пару (элемент, сосед),
        в случае неудачи - None.
        """
        empties = list(get_empty_cells(self.field))
        if empties:
            start = random.randint(0, len(empties) - 1)
            for head in empties[start:] + empties[:start]:
                if self.can_add_cell(head, self.number):
                    tail = self.get_path_extension_neighbour(head, self.number)
                    if tail is not None:
                        return head, tail
        return None

    def add_new_path(self, head, tail):
        number = self.number
        self.paths.append(Path(head))
        self.field[head] = self.field[tail] = number
        self.covered_cells += 2
        while True:
            head = tail
            tail = self.get_path_extension_neighbour(head, number)
            if tail is not None and self.covered_cells < self.cells_amount:
                self.field[tail] = number
                self.covered_cells += 1
            else:
                self.paths[-1].end = head
                return

    def get_field_with_pairs(self):
        field = generate_hexagonal_field(self.field.size)
        for i, path in enumerate(self.paths):
            for level, index in [path.start, path.end]:
                field[level][index] = i + 1
        return field

    def construct(self):
        while True:
            pair = self.try_get_new_path_begin()
            if pair is not None:
                self.add_new_path(*pair)
            else:
                if (self.covered_cells == self.cells_amount
                        and self.number <= MAX_NUMBER):
                    return self.get_field_with_pairs()
                else:
                    field = generate_hexagonal_field(self.field.size)
                    self.__init__(HexagonalField(field))


def count(iterable):
    return sum(1 for _ in iterable)


def centered_hex_number(n):
    return 3 * n * (n - 1) + 1


def get_empty_cells(field: HexagonalField):
    for i, level in enumerate(field.field):
        for j, cell in enumerate(level):
            if cell == CELL_EMPTY:
                yield i, j


def generate_hexagonal_field(size):
    distance = size - size // 2
    sequence = itertools.chain(range(distance, size),
                               range(size, distance - 1, -1))
    return [[0] * i for i in sequence]


def generate_field(size=None):
    size = size or random.randrange(MIN_SIZE, MAX_SIZE + 1, 2)
    field = generate_hexagonal_field(size)
    constructor = PathConstructor(HexagonalField(field))
    return constructor.construct()
