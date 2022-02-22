import sys

import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QTextEdit, QTableWidget, QLineEdit


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = []
        uic.loadUi('main.ui', self)
        self.update()
        self.pushButton_2.clicked.connect(self.edit)
        self.pushButton.clicked.connect(self.new)

    def update(self):
        title = ["ID", "название сорта", "степень обжарки",
                 "молотый/в зернах", "описание вкуса", "цена", "объем упаковки"]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)

        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()
        res3 = {i[0]: i[1] for i in cur.execute('SELECT * FROM types').fetchall()}
        res2 = {i[0]: i[1] for i in cur.execute('SELECT * FROM roast').fetchall()}

        for i, row in enumerate(result):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)

            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
                if j == 2:
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(res2[elem])))
                if j == 3:
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(res3[elem])))
        self.tableWidget.resizeColumnsToContents()
        con.close()

    def edit(self):
        lst = []
        for i in range(7):
            lst.append(self.tableWidget.item(self.tableWidget.currentRow(), i).text())
        self.second_form = NewWin(self, lst)
        self.second_form.show()

    def new(self):
        self.second_form = NewWin(self)
        self.second_form.show()


class NewWin(QMainWindow):
    def __init__(self, main_window, lst: list = None):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.flag = False
        if lst is not None:
            self.flag = True
            self.coffee_id = lst[0]
            self.lineEdit.setText(lst[1])
            self.lineEdit_2.setText(lst[2])
            self.lineEdit_3.setText(lst[3])
            self.textEdit.setText(lst[4])
            self.lineEdit_4.setText(lst[6])
            self.lineEdit_5.setText(lst[5])
        self.main_win = main_window

        self.pushButton_save.clicked.connect(self.save)
        # self.lineEdit = QLineEdit()

    def save(self):
        if self.flag:
            self.data()
        else:
            self.new_data()

    def data(self):
        coffee = self.lineEdit.text()
        coffee_index = self.lineEdit_2.text()
        coffee_type = self.lineEdit_3.text()
        coffee_taste = self.textEdit.toPlainText()
        coffee_price = int(self.lineEdit_4.text())
        coffee_v = int(self.lineEdit_5.text())
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        res = cur.execute(f"""SELECT id FROM types WHERE type = '{coffee_type}'""").fetchall()
        try:
            type_id = res[0][0]
        except IndexError as e:
            print(e)
            cur.execute(f"""INSERT INTO types(type) VALUES('{coffee_type}')""")
            con.commit()
            res = cur.execute(f"""SELECT id FROM types WHERE type = '{coffee_type}'""").fetchall()
            type_id = res[0][0]
        res = cur.execute(f"""SELECT id FROM roast WHERE type = '{coffee_index}'""").fetchall()
        try:
            index_id = res[0][0]
        except IndexError as e:
            print(e)
            cur.execute(f"""INSERT INTO roast(type) VALUES('{coffee_index}')""")
            con.commit()
            res = cur.execute(f"""SELECT id FROM roast WHERE type = '{coffee_index}'""").fetchall()
            index_id = res[0][0]

        cur.execute(f"""UPDATE coffee SET title =  '{coffee}', roast_degree = {index_id},
         type = {type_id}, taste = '{coffee_taste}',
                        prise = {coffee_price}, volume = {coffee_v} WHERE id = {self.coffee_id}""")
        con.commit()
        con.close()
        self.main_win.update()
        self.hide()

    def new_data(self):
        coffee = self.lineEdit.text()
        coffee_index = self.lineEdit_2.text()
        coffee_type = self.lineEdit_3.text()
        coffee_taste = self.textEdit.toPlainText()
        coffee_price = int(self.lineEdit_4.text())
        coffee_v = int(self.lineEdit_5.text())
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        res = cur.execute(f"""SELECT id FROM types WHERE type = '{coffee_type}'""").fetchall()
        try:
            type_id = res[0][0]
        except IndexError as e:
            print(e)
            cur.execute(f"""INSERT INTO types(type) VALUES('{coffee_type}')""")
            con.commit()
            res = cur.execute(f"""SELECT id FROM types WHERE type = '{coffee_type}'""").fetchall()
            type_id = res[0][0]
        res = cur.execute(f"""SELECT id FROM roast WHERE type = '{coffee_index}'""").fetchall()
        try:
            index_id = res[0][0]
        except IndexError as e:
            print(e)
            cur.execute(f"""INSERT INTO roast(type) VALUES('{coffee_index}')""")
            con.commit()
            res = cur.execute(f"""SELECT id FROM roast WHERE type = '{coffee_index}'""").fetchall()
            index_id = res[0][0]

        cur.execute(f"""INSERT INTO coffee(title, roast_degree, type, taste,
                        prise, volume) VALUES('{coffee}', {index_id},
                        {type_id}, '{coffee_taste}', {coffee_price}, {coffee_v})""")
        con.commit()
        con.close()
        self.main_win.update()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
