import sqlite3

import main
from PyQt5 import QtCore, uic
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget
from ut import algorithm, divide, similar


class Learn(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("designs/learn.ui", self)
        self.count = -1
        self.m = None
        self.con = sqlite3.connect("database.sqlite")
        self.cur = self.con.cursor()
        self.ratios = []
        self.proceedButton.clicked.connect(self.start_learning)
        self.checkButton.clicked.connect(self.check_correct)
        self.next.clicked.connect(self.start_learning)
        self.again.clicked.connect(self.start_checking)

    def setVariables(self, poem: list, verse_size: int, cur_id: int):
        self.verse_size = verse_size
        self.poem = list(divide(poem, verse_size))
        self.needed = algorithm(self.poem)
        self.id = cur_id

    def start_learning(self):
        """
        Start the learning process.

        This method is responsible for starting the learning process.
        It sets the current widget of the stacked widget to the first widget.
        It increments the count variable by 1.
        If the count is greater than or equal to the length of the needed list, it sets
        the text of the output widget to "Выучил. Молодец!" and returns.
        Otherwise, it sets the text of the output widget to the joined string of the
        the needed list at index count.
        If the length of the needed list at index count is greater than 4:
            - If it is also greater than 12, it sets the font of the output widget to
            "MS Shell Dlg" with a size of 12.
            - If it is also greater than 20, it sets the font of the output widget to
            "MS Shell Dlg" with a size of 8.
            - Otherwise, it sets the font of the output widget to "MS Shell Dlg"
            with a size of 16.
        It calls the start_checking method.
        """
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(0))
        self.checking.setText("")
        self.output.setFont(QFont("MS Shell Dlg", 24))
        self.count += 1
        if self.count >= len(self.needed):
            self.output.setText("Выучил. Молодец!\n Для выхода нажмите кнопку 'Выход'")
            self.proceedButton.setText("Выход")
            self.proceedButton.clicked.connect(self.exit_to_main_menu)
            return
        self.output.setText("\n".join(self.needed[self.count]))
        if len(self.needed[self.count]) > 4:
            if len(self.needed[self.count]) > 12:
                self.output.setFont(QFont("MS Shell Dlg", 12))
            elif len(self.needed[self.count]) > 20:
                self.output.setFont(QFont("MS Shell Dlg", 8))
            else:
                self.output.setFont(QFont("MS Shell Dlg", 16))
            self.start_checking()

    def start_checking(self):
        """
        Starts the checking process.

        This function sets the current widget of the stackedWidget to the first widget,
        sets the text of the label to "Повторение", hides the proceedButton,
        creates a QTimer object named 'tim' with an interval of 15000 milliseconds,
        starts the timer, and enters a while loop as long as the timer is active.

        Inside the loop, the text of the checking label is set to the remaining time in
        seconds, calculated by dividing the remaining time of the timer by 1000.
        If the remaining time is less than 10 milliseconds, the timer is stopped.

        The function then calls QtCore.QCoreApplication.processEvents() to process any
        pending events, making sure the GUI is updated.

        After the while loop, the proceedButton is made visible again,
        and the current widget is set to the second widget.
        """
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(0))
        self.label.setText("Повторение")
        self.proceedButton.setVisible(False)
        tim = QtCore.QTimer()
        tim.setInterval(10000)
        tim.start()
        while tim.isActive():
            self.checking.setText(f"Осталось {tim.remainingTime() // 1000} секунд.")
            if tim.remainingTime() < 10:
                tim.stop()
            QtCore.QCoreApplication.processEvents()
        self.proceedButton.setVisible(True)
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(1))

    def check_correct(self):
        """
        * Sets the current widget of the stackedWidget to the third widget.
        * Removes punctuation marks and converts strings to lowercase for comparison.
        * Calculates the correctness ratio between strings
        and formats it as a percentage.
        * Updates the text variable with the correctness ratio.
        * If the correctness ratio is above 0.75, sets the result label color to green
        and lets user proceed.
        * If the number of lines in the check string is less than or equal to half of the
        number of lines in the needed string, sets the result label color to red and
        hides the proceed button.
        * If the correctness ratio is above 0.5, sets the result label color to orange
        and lets user to make a choice.
        * If none of the above conditions are met, sets the result label color to red and
        hides the proceed button.
        * Updates the result label text with the calculated correctness ratio and
        additional messages based on the conditions.
        """
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
        text = f"Отношение правильности: {round(similar(to_check_with, ch) * 100, 2)}%"
        self.ratios.append(similar(to_check_with, ch))
        if similar(to_check_with, ch) > 0.75:
            self.result.setStyleSheet("color: green;")
            self.again.setVisible(False)
            text += "\nПрекрасная работа! Ты можешь продолжить изучение."
        elif len(ch.split("\n")) <= len(self.needed[self.count]) // 2:
            self.result.setStyleSheet("color: red;")
            self.next.setVisible(False)
            self.again.setVisible(True)
            text += (
                "\nТы написал менее половины строк. Тебе придётся повторить попытку."
            )
        elif similar(to_check_with, ch) > 0.5:
            self.result.setStyleSheet("color: orange;")
            text += (
                "\nНе очень хороший результат. Если хочешь, можешь повторить попытку."
            )
            self.next.setVisible(True)
            self.again.setVisible(True)
        else:
            self.result.setStyleSheet("color: red;")
            self.next.setVisible(False)
            self.again.setVisible(True)
            text += "\nТы сделал много ошибок. Тебе придётся повторить попытку."
        self.result.setText(text)

    def exit_to_main_menu(self):
        req = "UPDATE poem SET wrong_ratio = "
        req += f"{sum(self.ratios) / len(self.ratios)} WHERE id = {self.id}"
        self.cur.execute(req)
        if self.m is None:
            self.m = main.Main()
        self.con.commit()
        self.con.close()
        self.hide()
        self.m.show()
