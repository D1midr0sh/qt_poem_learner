import sys

import learn
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("designs/main.ui", self)
        self.w = None
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(0))
        self.learnButton.clicked.connect(self.setPoem)
        self.openFileBtn.clicked.connect(self.getPoemFromFile)
        self.readyButton.clicked.connect(self.proceed_to_learn)

    def setPoem(self):
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(1))

    def getPoemFromFile(self):
        """
        Reads a poem from a file selected by the user and displays it in the poem editor.

        :param self: The current instance of the class.
        :return: None
        """
        poem = QFileDialog.getOpenFileName(self)[0]
        with open(poem, "r", encoding="utf8") as f:
            self.poemEdit.setText(f.read())

    def proceed_to_learn(self):
        if self.w is None:
            self.w = learn.Learn()
        self.hide()
        self.w.setVariables(self.poemEdit.toPlainText().split("\n"), self.lines.value())
        self.w.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
