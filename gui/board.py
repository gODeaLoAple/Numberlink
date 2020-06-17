import functools
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from algorithms.solver import make_field_from_solution, solve
from numberlink import HexagonalField, HexLink


class CellButton(QPushButton):
    MAX_NUMBER = 9
    COLORS = [
        "white",
        "red",
        "green",
        "blue",
        "orange",
        "yellow",
        "purple",
        "grey",
        "brown",
        "pink"
    ]

    def __init__(self, position, parent):
        super().__init__("0", parent)
        self.position = position
        self.set_number(0)
        self.on_mouse_click = None

    @property
    def number(self):
        return int(self.text()) if self.text() else 0

    def to_next_number(self):
        self.set_number((self.number + 1) % (CellButton.MAX_NUMBER + 1))

    def to_previous_number(self):
        self.set_number((self.number - 1) % (CellButton.MAX_NUMBER + 1))

    def set_number(self, value):
        if value > CellButton.MAX_NUMBER:
            raise ValueError()
        self.setText(str(value) if value > 0 else "0")
        color = CellButton.COLORS[value]
        self.setStyleSheet(
            f"QPushButton {{ background-color: {color};}}"
        )

    def mousePressEvent(self, e):
        button = e.button()
        if button == Qt.LeftButton:
            self.to_next_number()
        elif button == Qt.RightButton:
            self.to_previous_number()
        if self.on_mouse_click:
            self.on_mouse_click()
        super().mousePressEvent(e)


class HexBoard(QWidget):
    def __init__(self, field, parent):
        super().__init__(parent)
        self.field = HexagonalField(field)
        self.board_size = self.field.size
        self.cells = []
        self.cell_length = 50
        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignCenter)
        for i, level in enumerate(self.field):
            hbox = QHBoxLayout(self)
            hbox.setAlignment(Qt.AlignCenter)
            for j, number in enumerate(level):
                cell = CellButton((i, j), self)
                cell.set_number(number)
                cell.setFixedSize(self.cell_length, self.cell_length)
                cell.on_mouse_click = functools.partial(self.cell_click, cell)
                self.cells.append(cell)
                hbox.addWidget(cell, 0, Qt.AlignCenter)
            vbox.addLayout(hbox)

        self.setLayout(vbox)

    def cell_click(self, cell):
        self.field[cell.position] = cell.number

    def clear(self):
        for cell in self.cells:
            cell.set_number(0)
            self.field[cell.position] = cell.number


class GameBoard(HexBoard):
    def __init__(self, field, parent):
        super().__init__(field, parent)
        self.field = HexLink(field)
        self.targets = self.field.get_targets()["vertices"]
        self.solutions = [
            HexagonalField(make_field_from_solution(self.field, solution))
            for solution in solve(self.field)
        ]
        self.when_solved = lambda: None

        for cell in self.cells:
            if cell.position in self.targets:
                cell.setEnabled(False)

    def cell_click(self, cell):
        if cell.position not in self.targets:
            super().cell_click(cell)
            if self.check_solution():
                self.when_solved()

    def check_solution(self):
        return any(self.field == solution for solution in self.solutions)

    def clear(self):
        for cell in self.cells:
            if cell.position not in self.targets:
                cell.set_number(0)
                self.field[cell.position] = 0

    def set_field(self, field):
        for i, level in enumerate(field):
            for j, cell in enumerate(level):
                self.field[i, j] = cell
        for cell in self.cells:
            cell.set_number(self.field[cell.position])
