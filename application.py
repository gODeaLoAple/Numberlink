import sys
from PyQt5.QtWidgets import QApplication
from gui.windows import NumberlinkWindow


if __name__ == "__main__":
    try:
        application = QApplication(sys.argv)
        window = NumberlinkWindow()
        sys.exit(application.exec())
    except Exception as e:
        print(e.args[0])
        sys.exit(-1)
