# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget


class main_window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


if __name__ == "__main__":
    app = QApplication([])
    window = main_window()
    window.show()
    sys.exit(app.exec())
