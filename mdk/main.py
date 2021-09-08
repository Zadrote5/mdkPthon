import MySQLdb
from PyQt5 import QtWidgets, uic, Qt
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize, Qt
import numpy
import sys

db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                     user="root",  # your username
                     passwd="root",  # your password
                     db="mdk")  # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()


def get_list_materials():
    cur.execute("SELECT * FROM material")
    return cur.fetchall()


def delete_material(id):
    query = "DELETE FROM material WHERE id = " + str(id)
    return cur.execute(query)


def add_material(title, count_pack, unit, count_stock, min_count, description, cost, image, material_type):
    query = """INSERT INTO material
            (Title, CountinPack, Unit, CountInStock, MinCount, Description, Cost, Image, MaterialTypeId)
             values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (title, count_pack, unit, count_stock, min_count, description, cost, image, material_type)
    cur.execute(query, values)
    return db.commit()





class MainWindow(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(1150, 800))  # Устанавливаем размеры
        self.setWindowTitle("MDK")  # Устанавливаем заголовок окна
        central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(central_widget)  # Устанавливаем центральный виджет

        grid_layout = QGridLayout()  # Создаём QGridLayout
        central_widget.setLayout(grid_layout)  # Устанавливаем данное размещение в центральный виджет

        material = get_list_materials()
        listin = list(material)

        table = QTableWidget(self)  # Создаём таблицу
        table.setColumnCount(len(listin[0]))  # Устанавливаем колонки
        table.setRowCount(len(listin))  # и одну строку в таблице

        # Устанавливаем заголовки таблицы
        table.setHorizontalHeaderLabels(["ID", "Название", "Количество в упаковке", "Единица измерения",
                                         "Остаток в наличии", "Минимальное количество", "Описание",
                                         "Цена", "Путь до изображения", "айди материала"])

        # Устанавливаем всплывающие подсказки на заголовки
        table.horizontalHeaderItem(0).setToolTip("ID")
        table.horizontalHeaderItem(1).setToolTip("Название")
        table.horizontalHeaderItem(2).setToolTip("Количество в упаковке")


        # Устанавливаем выравнивание на заголовки
        table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignRight)

        # заполняем первую строку

        for i in range(len(listin)):
            for j in range(len(listin[i])):
                table.setItem(i, j, QTableWidgetItem(str(listin[i][j])))






        # делаем ресайз колонок по содержимому
        table.resizeColumnsToContents()

        grid_layout.addWidget(table, 0, 0)  # Добавляем таблицу в сетку


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())



db.close()