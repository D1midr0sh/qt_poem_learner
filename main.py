import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("designs/main.ui", self)
        self.learnButton.clicked.connect(self.setPoem)
        self.openFileBtn.clicked.connect(self.getPoemFromFile)

    def setPoem(self):
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(1))

    def getPoemFromFile(self):
        poem = QFileDialog.getOpenFileName(self)[0]
        with open(poem, "r", encoding="utf8") as f:
            self.poemEdit.setText(f.read())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
