from PyQt5 import QtCore, uic
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget
from ut import algorithm, divide, similar


class Learn(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("designs/learn.ui", self)
        self.count = -1
        self.proceedButton.clicked.connect(self.start_learning)
        self.checkButton.clicked.connect(self.check_correct)

    def setVariables(self, poem: list, verse_size: int):
        self.verse_size = verse_size
        self.poem = list(divide(poem, verse_size))
        self.needed = algorithm(self.poem)

    def start_learning(self):
        self.checking.setText("")
        self.output.setFont(QFont("MS Shell Dlg", 24))
        self.count += 1
        if self.count >= len(self.needed):
            self.output.setText("Выучил. Молодец!")
            return
        self.output.setText("\n".join(self.needed[self.count]))
        if len(self.needed[self.count]) > 4:
            if len(self.needed[self.count]) > 12:
                self.output.setFont(QFont("MS Shell Dlg", 12))
            elif len(self.needed[self.count]) > 20:
                self.output.setFont(QFont("MS Shell Dlg", 8))
            else:
                self.output.setFont(QFont("MS Shell Dlg", 16))
            self.label.setText("Повторение")
            self.proceedButton.setVisible(False)
            tim = QtCore.QTimer()
            tim.setInterval(15000)
            tim.start()
            while tim.isActive():
                self.checking.setText(f"Осталось {tim.remainingTime() // 1000} секунд.")
                if tim.remainingTime() < 10:
                    tim.stop()
                QtCore.QCoreApplication.processEvents()
            self.proceedButton.setVisible(True)
            self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(1))

    def check_correct(self):
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(2))
        to_check_with = (
            "\n".join(self.needed[self.count]).replace(".", "").replace(",", "")
        )
        to_check_with = (
            to_check_with.replace("!", "")
            .replace("?", "")
            .replace(":", "")
            .replace(";", "")
        )
        to_check_with = (
            to_check_with.replace("-", "").replace("(", "").replace(")", "").lower()
        )
        ch = (
            self.check.toPlainText()
            .replace(".", "")
            .replace(",", "")
            .replace("!", "")
            .replace("?", "")
        )
        ch = (
            ch.replace(":", "")
            .replace(";", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
            .lower()
        )
        self.result.setText(
            f"Отношение правильности: {round(similar(to_check_with, ch) * 100, 2)}%"
        )
