import random
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
                             QMessageBox, QDialog, QLabel, QMainWindow,
                             QStackedWidget)
from algorithms.generator import generate_hexagonal_field, generate_field
from gui.board import HexBoard, GameBoard
from numberlink import HexLink

FIELD_SIZE = 5


class MainMenu(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        play_button = QPushButton("Играть", self)
        play_button.clicked.connect(self.window().play)
        exit_button = QPushButton("Выход", self)
        exit_button.clicked.connect(self.window().exit)

        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignCenter)
        vbox.addWidget(play_button, 0, Qt.AlignCenter)
        vbox.addWidget(exit_button, 0, Qt.AlignCenter)


class LevelMenu(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        create_button = QPushButton("Создать уровень", self)
        create_button.clicked.connect(self.window().create_level)

        generate_button = QPushButton("Рандомный уровень", self)
        generate_button.clicked.connect(self.window().generate_level)

        back_button = QPushButton("Назад", self)
        back_button.clicked.connect(self.window().go_back)

        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignCenter)
        vbox.addWidget(create_button, 0, Qt.AlignCenter)
        vbox.addWidget(generate_button, 0, Qt.AlignCenter)
        vbox.addWidget(back_button, 0, Qt.AlignCenter)


class CreationMenu(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        field = generate_hexagonal_field(FIELD_SIZE)
        self.board = HexBoard(field, self)
        self.init_ui()

    def init_ui(self):
        accept_button = QPushButton("Принять", self)
        accept_button.clicked.connect(self.accept)

        cancel_button = QPushButton("Назад", self)
        cancel_button.clicked.connect(self.cancel)

        clear_button = QPushButton("Очистить", self)
        clear_button.clicked.connect(self.board.clear)

        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignCenter)
        hbox.addWidget(accept_button, 0, Qt.AlignCenter)
        hbox.addWidget(cancel_button, 0, Qt.AlignCenter)
        hbox.addWidget(clear_button, 0, Qt.AlignCenter)

        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.board, 0, Qt.AlignCenter)
        vbox.addLayout(hbox)

    def cancel(self):
        self.board.clear()
        self.window().go_back()

    def accept(self):
        try:
            HexLink.check_field(self.board.field.field)
            self.window().load_game(self.board.field.field)
            self.board.clear()
        except Exception as e:
            self.show_message(e.args[0])

    def show_message(self, text):
        msg = QMessageBox(self)
        msg.setWindowTitle("Ошибка")
        msg.setText(text)
        msg.setIcon(QMessageBox.Information)
        msg.show()


class GameWindow(QWidget):
    def __init__(self, field, parent):
        super().__init__(parent)
        self.board = GameBoard(field, self)
        self.init_ui()

    def init_ui(self):
        solve_button = QPushButton("Решение", self)
        solve_button.clicked.connect(self.solve)
        menu_button = QPushButton("Меню", self)
        menu_button.clicked.connect(self.window().menu)
        clear_button = QPushButton("Очистить", self)
        clear_button.clicked.connect(self.clear)

        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignCenter)
        hbox.addWidget(solve_button, 0, Qt.AlignCenter)
        hbox.addWidget(clear_button, 0, Qt.AlignCenter)
        hbox.addWidget(menu_button, 0, Qt.AlignCenter)

        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.board, 0, Qt.AlignCenter)
        vbox.addLayout(hbox)

        self.board.when_solved = self.show_finish_dialog

    def show_finish_dialog(self):
        msb = QDialog(self)
        msb.resize(100, 100)
        msb.setWindowTitle("Поздравляем!")
        msb.show()

        text = QLabel()
        text.setText("Вы решили задачу")

        return_button = QPushButton("Вернуться", msb)
        return_button.clicked.connect(msb.close)

        menu_button = QPushButton("Меню", msb)
        menu_button.clicked.connect(self.window().menu)
        menu_button.clicked.connect(msb.close)

        hbox = QHBoxLayout(self)
        hbox.addWidget(return_button, 0, Qt.AlignCenter)
        hbox.addWidget(menu_button, 0, Qt.AlignCenter)

        vbox = QVBoxLayout(msb)
        vbox.addWidget(text, 0, Qt.AlignCenter)
        vbox.addLayout(hbox)

    def solve(self):
        if not self.board.solutions:
            self.show_no_solutions()
        else:
            index = random.randint(0, len(self.board.solutions) - 1)
            self.board.set_field(self.board.solutions[index].field)

    def show_no_solutions(self):
        msg = QMessageBox()
        msg.setWindowTitle("Упс...")
        msg.setIcon(QMessageBox.Information)
        msg.setText("К сожалению, решений нет")
        msg.show()

    def clear(self):
        self.board.clear()


class NumberlinkWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_menu = MainMenu(self)
        self.level_menu = LevelMenu(self)
        self.creation_menu = CreationMenu(self)
        self.game = None
        self.history = []
        self.init_ui()

    def init_ui(self):
        self.resize(600, 500)
        self.show()
        self.setWindowTitle("HexLink")

        stacked_widget = QStackedWidget(self)
        self.setCentralWidget(stacked_widget)
        self.centralWidget().addWidget(self.main_menu)
        self.centralWidget().addWidget(self.level_menu)
        self.centralWidget().addWidget(self.creation_menu)
        self.menu()

    def menu(self):
        self.history.clear()
        self.centralWidget().setCurrentWidget(self.main_menu)

    def play(self):
        self.history.append(self.centralWidget().currentWidget())
        self.centralWidget().setCurrentWidget(self.level_menu)

    def create_level(self):
        self.history.append(self.centralWidget().currentWidget())
        self.centralWidget().setCurrentWidget(self.creation_menu)

    def generate_level(self):
        self.history.clear()
        self.game = GameWindow(generate_field(FIELD_SIZE), self)
        self.centralWidget().addWidget(self.game)
        self.centralWidget().setCurrentWidget(self.game)

    def load_game(self, field):
        self.history.clear()
        self.game = GameWindow(field, self)
        self.centralWidget().addWidget(self.game)
        self.centralWidget().setCurrentWidget(self.game)

    def go_back(self):
        self.centralWidget().setCurrentWidget(self.history.pop())

    def exit(self):
        self.close()
