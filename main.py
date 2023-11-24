import sqlite3
import sys

import learn
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
import stats


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("designs/main.ui", self)
        self.con = sqlite3.connect("database.sqlite")
        self.cur = self.con.cursor()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS poem
                            (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            name TEXT,
                            author TEXT,
                            wrong_ratio REAL,
                            mistakes INTEGER)"""
        )
        self.con.commit()
        self.w = None
        self.s = None
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(0))
        self.learnButton.clicked.connect(self.setPoem)
        self.openFileBtn.clicked.connect(self.getPoemFromFile)
        self.readyButton.clicked.connect(self.proceed_to_learn)
        self.statsButton.clicked.connect(self.go_to_stats)

    def setPoem(self):
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(1))

    def getPoemFromFile(self):
        """
        Reads a poem from a file selected by the user and displays it in the poem editor.
        """
        poem = QFileDialog.getOpenFileName(self)[0]
        with open(poem, "r", encoding="utf8") as f:
            self.poemEdit.setText(f.read())

    def proceed_to_learn(self):
        errors = ""
        if self.poemEdit.toPlainText() == "":
            errors += "* Вы не ввели стих\n"
        if self.nameEdit.toPlainText() == "":
            errors += "* Вы не ввели название\n"
        if self.authorEdit.toPlainText() == "":
            errors += "* Вы не ввели автора\n"
        if len(self.poemEdit.toPlainText().split("\n")) < self.lines.value():
            errors += "* Слишком мало строк\n"
        if len(self.poemEdit.toPlainText().split("\n")) % self.lines.value() != 0:
            errors += "* Количество строк не кратно\nколичеству строк в строфе\n"
        if errors != "":
            self.errorLabel.setText(errors)
            self.errorLabel.setStyleSheet("color: red;")
            return
        id = self.cur.execute("SELECT max(id) FROM poem").fetchone()[0]
        if id is None:
            id = 0
        else:
            id += 1
        data = (
            id,
            self.nameEdit.toPlainText(),
            self.authorEdit.toPlainText(),
            0,
            0,
        )
        self.cur.execute("""INSERT INTO poem VALUES (?, ?, ?, ?, ?)""", data)
        self.con.commit()
        if self.w is None:
            self.w = learn.Learn()
        self.hide()
        self.w.setVariables(
            self.poemEdit.toPlainText().split("\n"), self.lines.value(), id
        )
        self.w.show()
        self.con.close()

    def go_to_stats(self):
        if self.s is None:
            self.s = stats.Stats()
        self.hide()
        self.s.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
