from PyQt5 import uic
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget
from ut import algorithm, divide


class Learn(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("designs/learn.ui", self)
        self.count = -1
        self.proceedButton.clicked.connect(self.start_learning)

    def setVariables(self, poem: list, verse_size: int):
        self.verse_size = verse_size
        self.poem = list(divide(poem, verse_size))
        self.needed = algorithm(self.poem)

    def start_learning(self):
        self.count += 1
        if self.count >= len(self.needed):
            self.output.setText("Выучил. Молодец!")
        self.output.setText('\n'.join(self.needed[self.count]))
        if len(self.needed[self.count]) > 4:
            self.output.setFont(QFont("MS Shell Dlg", 16))
