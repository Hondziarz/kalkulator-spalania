import sqlite3
from datetime import date

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel,QGridLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton
from PyQt5.QtWidgets import QMessageBox,QComboBox
from PyQt5.QtCore import Qt, pyqtSignal

import matplotlib.pyplot as plt
import sys


class SecondWindowStatistics(QWidget):
    window2_closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.interface()

    def interface(self):
        self.setGeometry(30, 20, 500, 200)
        self.setWindowTitle("kalkulator")
        main_grid = QGridLayout()
        self.setLayout(main_grid)

        label1 = QLabel("Add new car")
        label2 = QLabel("Model", self)
        label3 = QLabel("Milage", self)
        button_add_car = QPushButton("&Add", self)
        self.text1 = QLineEdit()
        self.text2 = QLineEdit()

        main_grid.addWidget(label1, 0, 1)
        main_grid.addWidget(label2, 1, 0)
        main_grid.addWidget(label3, 2, 0)
        main_grid.addWidget(self.text1, 1, 1)
        main_grid.addWidget(self.text2, 2, 1)
        main_grid.addWidget(button_add_car, 3, 1)
        button_add_car.setMinimumWidth(520)

        button_add_car.clicked.connect(self.add_car)

        return main_grid

    def add_car(self):

        self.con = sqlite3.connect('test2.db')
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        self.cur.execute("INSERT INTO samochod VALUES(NULL, ?, ?);", (self.text1.text(), self.text2.text()))
        self.con.commit()
        self.close()

    def closeEvent(self, event):
        self.window2_closed.emit()
        event.accept()


class ThirdWindowStatistics(QWidget):
    window3_closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.interface()

    def interface(self):
        self.setGeometry(30, 20, 500, 200)
        self.setWindowTitle("kalkulator")
        main_grid = QGridLayout()
        self.setLayout(main_grid)

        label1=QLabel("Check car",self)
        label1.setAlignment(Qt.AlignCenter)
        delete_button = QPushButton("&Delete", self)
        self.cb = QComboBox()

        main_grid.addWidget(label1,0,0)
        main_grid.addWidget(self.cb,1,0)
        main_grid.addWidget(delete_button,2,0)

        delete_button.clicked.connect(self.delete_car)

        self.check_car()
        return main_grid

    def check_car(self):
        self.con = sqlite3.connect('test2.db')
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        self.cur.execute("""
                                            CREATE TABLE IF NOT EXISTS samochod (
                                                id INTEGER PRIMARY KEY ASC,
                                                marka varchar(250) NOT NULL,
                                                przebieg INTEGER NOT NULL
                                            )""")

        self.cur.execute(
            """
            SELECT marka, przebieg FROM samochod
            """
        )
        cars = self.cur.fetchall()
        for car in cars:
            self.cb.addItem(car["marka"])

        return self.cb

    def delete_car(self):
        self.con = sqlite3.connect('test2.db')
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        car = self.cb.currentText()

        self.cur.execute("DELETE FROM samochod WHERE marka =?", (car,))
        self.con.commit()
        self.close()

    def closeEvent(self, event):
        self.window3_closed.emit()
        event.accept()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.interface()

    def interface(self):

        main_grid = QGridLayout()

        self.setGeometry(30, 20, 500, 200)
        self.setWindowTitle("calculator")

        main_grid.addLayout(self.maingroup(), 0, 0)
        main_grid.addLayout(self.secondgroup(),0,1)
        main_grid.addLayout(self.thirdgroup(),1,0,1,2)

        self.setLayout(main_grid)

    def maingroup(self):

        uklad_t = QGridLayout()

        label1 = QLabel("Kilometers traveled:", self)
        self.kilometers_travelled_edit = QLineEdit()
        label2 = QLabel("Liters of fuel:", self)
        self.liters_edit = QLineEdit()
        label3 = QLabel("Fuel price:", self)
        self.fuel_price_edit = QLineEdit()

        uklad_t.addWidget(label1, 0, 0)
        uklad_t.addWidget(self.kilometers_travelled_edit, 0, 1)
        uklad_t.addWidget(label2, 1, 0)
        uklad_t.addWidget(self.liters_edit, 1, 1)
        uklad_t.addWidget(label3, 2, 0)
        uklad_t.addWidget(self.fuel_price_edit, 2, 1)

        result_button = QPushButton("&Result", self)
        uklad_t.addWidget(result_button, 3, 0, 1, 2)

        add_data_button = QPushButton("&Add data to datebase", self)
        add_data_button.setStyleSheet("background-color : red")
        uklad_t.addWidget(add_data_button, 6, 0, 1, 2)

        add_data_button.clicked.connect(self.make_sure)

        label4 = QLabel("average fuel consumption is", self)
        label5 = QLabel("the cost of driving 100 km:", self)

        uklad_t.addWidget(label4, 4, 0)
        uklad_t.addWidget(label5, 4, 1)

        self.fuel_usage = QLineEdit()
        self.cost = QLineEdit()
        self.fuel_usage.readonly = True
        self.cost.readonly = True

        uklad_t.addWidget(self.fuel_usage, 5, 0)
        uklad_t.addWidget(self.cost, 5, 1)

        result_button.clicked.connect(self.dzialanie)

        return uklad_t

    def cbmake(self):
        self.con = sqlite3.connect('test2.db')
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        self.cur.execute("""
                                    CREATE TABLE IF NOT EXISTS samochod (
                                        id INTEGER PRIMARY KEY ASC,
                                        marka varchar(250) NOT NULL,
                                        przebieg INTEGER NOT NULL
                                    )""")

        self.cur.execute(
            """
            SELECT marka, przebieg FROM samochod
            """
        )
        cars = self.cur.fetchall()
        for car in cars:
            self.cb.addItem(car["marka"])

        return self.cb

    def secondgroup(self):

        ukladX = QGridLayout()
        label0 = QLabel("select a vehicle:")
        add_car = QPushButton("Add new car")
        delete_car = QPushButton("Delete car")

        self.cb = QComboBox()
        add_car.clicked.connect(self.show_new_window_add_car)
        delete_car.clicked.connect(self.show_new_window_delete_car)

        ukladX.addWidget(label0,0,0)
        ukladX.addWidget(self.cb,1,0)
        ukladX.addWidget(add_car,2,0)
        ukladX.addWidget(delete_car,3,0)


        self.cbmake()

        return ukladX

    def show_new_window_add_car(self):
        self.w = SecondWindowStatistics()
        self.cb.clear()
        self.w.window2_closed.connect(self.cbmake)
        self.w.show()

    def show_new_window_delete_car(self):
        self.w = ThirdWindowStatistics()
        self.cb.clear()
        self.w.window3_closed.connect(self.cbmake)
        self.w.show()

    def thirdgroup(self):

        layout = QGridLayout()

        read_data_consumption = QPushButton("Read the data", self)
        read_data_price = QPushButton("Read the data", self)
        read_data = QPushButton("Read the data", self)

        layout.addWidget(read_data, 0, 1)
        layout.addWidget(read_data, 0, 2)
        layout.addWidget(read_data, 0, 3)


        read_data.clicked.connect(self.make_chart)


        return layout

    def add_car(self):

        car = self.model.text()
        milage = float(self.przebieg.text())

        self.cur.execute("INSERT INTO samochod VALUES(NULL, ?, ?);", (car, milage))
        self.cb.addItem(car)
        self.con.commit()



    def make_chart(self):
        car = self.cb.currentText()
        self.cur.execute("SELECT id FROM samochod WHERE marka = ?", (car,))
        car_id = self.cur.fetchone()
        car_id= car_id[0]

        self.cur.execute("SELECT data, spalanie FROM spalanie WHERE car_id = ?", (car_id,))
        data = self.cur.fetchall()
        c = []
        d = []
        for a in data:
            c.append(a["data"])
            d.append(a["spalanie"])

        plt.plot(c, d)
        plt.show()

    def datebase_updating(self):
        kilometers_amount = int(self.kilometers_travelled_edit.text())
        fuel_usage = self.fuel_usage.text()
        today = date.today()
        auto = self.cb.currentText()

        self.cur.execute("SELECT id, przebieg FROM samochod WHERE marka = ?", (auto,))
        car_data = self.cur.fetchone()
        id_car = car_data[0]
        milage = car_data[1]
        updated_milage = milage + kilometers_amount



        self.cur.execute("""
                            CREATE TABLE IF NOT EXISTS spalanie (
                            id INTEGER PRIMARY KEY ASC,
                            przebieg INT NOT NULL,
                            data DATE  NOT NULL,
                            spalanie FLOAT NOT NULL,
                            car_id INTEGER NOT NULL,
                            FOREIGN KEY(car_id) REFERENCES samochod(id)
                            )""")

        self.con.commit()



        self.cur.execute('INSERT INTO spalanie VALUES(NULL, ?, ?, ?,?);', (updated_milage,today, fuel_usage,id_car,))
        self.cur.execute('UPDATE samochod SET przebieg=? WHERE id=?', (updated_milage, id_car))
        self.con.commit()

    def make_sure(self):
        odp = QMessageBox.question(
            self, "komunikat", "Czy na pewno dodać?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.No)
        if odp == QMessageBox.Yes:
            if len(self.fuel_usage.text()) != 0 and len(self.cost.text()) != 0:
                self.datebase_updating()
            else:
                QMessageBox.warning(self, "Błąd", "Błędne dane", QMessageBox.Ok)
        else:
            pass

    def dzialanie(self):
        sender = self.sender()

        try:
            kilometers_amount = float(self.kilometers_travelled_edit.text())
            liters_amount = float(self.liters_edit.text())
            fuel_price = float(self.fuel_price_edit.text())
            average_consumption = ""
            cost_per_100km = ""

            if sender.text() == "&Result":

                try:
                    average_consumption = round(liters_amount / kilometers_amount * 100, 8)
                    cost_per_100km = average_consumption*fuel_price



                except ZeroDivisionError:
                    QMessageBox.critical(
                        self, "Błąd", "Nie można dzielić przez zero!")
                    return

            self.fuel_usage.setText(str(average_consumption))
            self.cost.setText(str(cost_per_100km))

        except ValueError:
            QMessageBox.warning(self, "Błąd", "Błędne dane", QMessageBox.Ok)

    def finish(self):
        self.close()

    def closeEvent(self, event):
        question = QMessageBox.question(
            self, "komunikat", "Czy na pewno koniec?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.No)
        if question == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.finish()
        else:
            QMessageBox.warning(self, "Błąd", "Błędne dane", QMessageBox.Ok)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    okno = MainWindow()
    okno.show()
    sys.exit(app.exec_())