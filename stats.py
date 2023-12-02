import sqlite3

import main
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class Stats(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("designs/stats.ui", self)
        self.backButton.clicked.connect(self.exit_to_main_menu)
        self.con = sqlite3.connect("database.sqlite")
        self.cur = self.con.cursor()
        self.m = None
        cur_id = self.cur.execute("""SELECT MAX(id) FROM poem""").fetchone()[0]
        if cur_id is None:
            self.lastPoem.setText("В базе нет ни одного стиха")
            return
        self.cur.execute("""SELECT * FROM poem WHERE id = ?""", (cur_id,))
        poem = self.cur.fetchone()
        self.lastPoem.setText(f"Последний изученный стих: {poem[1]}\nАвтор: {poem[2]}")
        self.cur.execute("""SELECT AVG(wrong_ratio) FROM poem""")
        avg = round(self.cur.fetchone()[0], 2)
        self.avgRatio.setText(f"Средний коэффициент правильности за все стихи: {avg}")
        req = "SELECT * FROM poem WHERE mistakes = (SELECT MIN(mistakes) FROM poem)"
        self.cur.execute(req)
        poem = self.cur.fetchone()
        self.leastMistakes.setText(
            f"Стих с наименьшим количеством ошибок ({poem[4]}):\n{poem[1]}, {poem[2]}"
        )
        req = "SELECT AVG(mistakes) FROM poem"
        self.cur.execute(req)
        avg = round(self.cur.fetchone()[0], 2)
        self.avgMistakes.setText(f"Среднее количество ошибок за все стихи: {avg}")

    def exit_to_main_menu(self):
        self.con.close()
        if self.m is None:
            self.m = main.Main()
        self.hide()
        self.m.show()
