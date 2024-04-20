import sys
import pyodbc
from PyQt5 import QtWidgets
from DB_functions import *
#from ui import Ui_MainWindow as Ui_MainWindow2
from ui1 import Ui_MainWindow as Ui_MainWindow1
from ui2 import Ui_MainWindow as Ui_MainWindow3
from ui3 import Ui_MainWindow as Ui_MainWindow
from final_interface import Ui_MainWindow as Ui_MainWindow2
from datetime import datetime

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow2()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.current_page_index = 0
        self.ui.stackedWidget.setCurrentIndex(self.current_page_index)
        self.ui.back.clicked.connect(self.previous_page)
        self.ui.forward.clicked.connect(self.next_page)
        self.ui.add_tech.clicked.connect(self.add_row)
        self.ui.delete_tech.clicked.connect(self.delete_row)
        self.ui.add_os.clicked.connect(self.open_os_window)
        self.ui.delete_os.clicked.connect(self.delete_os)
        self.ui.post_new_emp.clicked.connect(self.add_data)
        self.ui.table_os.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.update_button_positions()

    def add_data(self):
        kab = int(self.ui.office.text())
        street = self.ui.street.text()
        home  = self.ui.house_num.text()
        surname = self.ui.surname.text()
        name = self.ui.name.text()
        patronymic = self.ui.patronymic.text()
        birthday = self.ui.born_date.text()
        gender = "M" if self.ui.gender_M.setChecked(True) else "Ж"
        post = self.ui.post.text()
        rank = self.ui.rank.text()
        division = self.ui.division.text()
        region = self.ui.region.text()
        phone_number = self.ui.phone_number.text()
        SNILS = self.ui.snils.text()
        insert_to_kab(kab, street, home)
        print(surname, name, patronymic, birthday, gender, post, rank, division, region, phone_number, SNILS)
        insert_to_employee(surname, name, patronymic, birthday, gender, post, rank, division, region, phone_number, SNILS)
        model = self.ui.model.text()
        invent_num = self.ui.invent_num.text()
        IP = self.ui.IP.text()
        virtual_IP = self.ui.virtual_IP.text()
        kab_code = get_id_kab()
        emp_code = get_id_emp()
        insert_to_sys_unit(model, invent_num, IP, virtual_IP, kab_code, emp_code)


    def previous_page(self):
        if self.current_page_index > 0:
            self.current_page_index -= 1
            self.ui.stackedWidget.setCurrentIndex(self.current_page_index)
            self.update_button_positions()

    def next_page(self):
        if self.current_page_index < 9:
            self.current_page_index += 1
            self.ui.stackedWidget.setCurrentIndex(self.current_page_index)
            self.update_button_positions()

    def update_button_positions(self):
        if self.current_page_index == 0:
            self.ui.back.setGeometry(0, 0, 0, 0)
            self.ui.forward.setGeometry(405, 615, 251, 81)
        elif self.current_page_index == 4:
            self.ui.back.setGeometry(405, 615, 251, 81)
            self.ui.forward.setGeometry(0, 0, 0, 0)
        else:
            self.ui.back.setGeometry(405, 615, 101, 81)
            self.ui.forward.setGeometry(555, 615, 101, 81)

    def add_row(self):
        row_count = self.ui.table_tech.rowCount()
        self.ui.table_tech.insertRow(row_count)

    def delete_row(self):
        selected_row = self.ui.table_tech.currentRow()
        if selected_row != -1:
            self.ui.table_tech.removeRow(selected_row)
        else:
            row_count = self.ui.table_tech.rowCount()
            if row_count > 0:
                self.ui.table_tech.removeRow(row_count - 1)

    def open_os_window(self):
        self.os_window = OSWindow()
        self.os_window.ui.listWidget.itemClicked.connect(self.handle_os_item_click)
        self.os_window.show()

    def delete_os(self):
        selected_row = self.ui.table_os.currentRow()
        if selected_row != -1:
            self.ui.table_os.removeRow(selected_row)
        else:
            row_count = self.ui.table_os.rowCount()
            if row_count > 0:
                self.ui.table_os.removeRow(row_count - 1)



    def handle_os_item_click(self, item):
        selected_os = item.text()
        row_count = self.ui.table_os.rowCount()
        self.ui.table_os.insertRow(row_count)
        self.ui.table_os.setItem(row_count, 0, QtWidgets.QTableWidgetItem(selected_os))
        # Обновляем значение выбранного инвентарного номера при выборе операционной системы
        self.selected_inventory_number = selected_os

class OSWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow1()
        self.ui.setupUi(self)

class SearchWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow3()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.search)
        self.ui.pushButton_2.clicked.connect(self.open_main_window)
        self.ui.tableWidget.setColumnWidth(0, 45)
        self.ui.tableWidget.setColumnWidth(1, 140)
        self.ui.tableWidget.setColumnWidth(2, 140)
        self.ui.tableWidget.setColumnWidth(3, 150)
        self.ui.tableWidget.setColumnWidth(4, 140)
        self.ui.tableWidget.setColumnWidth(5, 235)

        self.db_connection = pyodbc.connect(
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=C:\Users\lenovo\PycharmProjects\MVDFinal\MVD.accdb;'
        )
        self.selected_inventory_number = None

        # Устанавливаем обработчик событий для таблицы
        self.ui.tableWidget.itemClicked.connect(self.handle_table_item_click)

    def search(self):
        query = """
            SELECT Сотрудники.[Кодсотрудника], Сотрудники.Фамилия, Сотрудники.Имя, Сотрудники.Отчество, Сотрудники.СНИЛС, СистемныеБлоки.ИнвентарныйНомер
            FROM Сотрудники
            INNER JOIN СистемныеБлоки ON Сотрудники.[Кодсотрудника] = СистемныеБлоки.[Кодсотрудника]
        """
        conditions = []
        params = []

        if self.ui.lineEdit.text():
            conditions.append("Сотрудники.Фамилия LIKE ?")
            params.append(f"%{self.ui.lineEdit.text()}%")
        if self.ui.lineEdit_2.text():
            conditions.append("Сотрудники.Имя LIKE ?")
            params.append(f"%{self.ui.lineEdit_2.text()}%")
        if self.ui.lineEdit_3.text():
            conditions.append("Сотрудники.Отчество LIKE ?")
            params.append(f"%{self.ui.lineEdit_3.text()}%")
        if self.ui.lineEdit_4.text():
            conditions.append("Сотрудники.СНИЛС LIKE ?")
            params.append(f"%{self.ui.lineEdit_4.text()}%")
        if self.ui.lineEdit_5.text():
            conditions.append("СистемныеБлоки.ИнвентарныйНомер LIKE ?")
            params.append(f"%{self.ui.lineEdit_5.text()}%")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cursor = self.db_connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()

        self.ui.tableWidget.setRowCount(0)

        for row_num, row_data in enumerate(result):
            self.ui.tableWidget.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                self.ui.tableWidget.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(str(col_data)))

    # Обработчик событий для таблицы
    def handle_table_item_click(self, item):
        selected_row = item.row()
        self.selected_inventory_number = self.ui.tableWidget.item(selected_row, 5).text()
        print("Выбранный инвентарный номер:", self.selected_inventory_number)  # Выводим для отладки

    def open_main_window(self):
        if self.selected_inventory_number:
            query = """
                SELECT Сотрудники.[Кодсотрудника], Сотрудники.Фамилия, Сотрудники.Имя, Сотрудники.Отчество,
                 Сотрудники.ДатаРождения, Сотрудники.Пол, Сотрудники.Должность, Сотрудники.Звание,
                  Сотрудники.Подразделение, Сотрудники.Регион, Сотрудники.Телефон, Сотрудники.СНИЛС,
                   СистемныеБлоки.Модель, СистемныеБлоки.ИнвентарныйНомер, СистемныеБлоки.IP,
                    СистемныеБлоки.[ВиртуальныйIP], Кабинеты.Номер, Кабинеты.Улица, Кабинеты.Дом
                FROM ((Сотрудники
                INNER JOIN СистемныеБлоки ON Сотрудники.[Кодсотрудника] = СистемныеБлоки.[Кодсотрудника])
                INNER JOIN Кабинеты ON СистемныеБлоки.[Кодкабинета] = Кабинеты.[Кодкабинета])
                WHERE СистемныеБлоки.ИнвентарныйНомер = ?
            """
            cursor = self.db_connection.cursor()
            cursor.execute(query, (self.selected_inventory_number,))
            result = cursor.fetchone()
            print("Результат запроса:", result)

            if result:
                self.main_window = MainWindow()
                self.main_window.ui.surname.setText(result[1])  # Фамилия
                self.main_window.ui.name.setText(result[2])  # Имя
                self.main_window.ui.patronymic.setText(result[3])  # Отчество
                self.main_window.ui.born_date.setText(str(result[4])[:-9].replace("-", "."))  # Дата рождения

                if result[5] == 'М':
                    self.main_window.ui.gender_M.setChecked(True)  # Пол
                else:
                    self.main_window.ui.gender_W.setChecked(True)

                self.main_window.ui.post.setText(result[6])  # Должность
                self.main_window.ui.rank.setText(result[7])  # Звание
                self.main_window.ui.division.setText(result[8])  # Подразделение
                self.main_window.ui.region.setText(result[9])  # Регион
                self.main_window.ui.phone_number.setText(result[10])  # Телефон
                self.main_window.ui.snils.setText(result[11])  # СНИЛС

                self.main_window.ui.model.setText(result[12])  # Модель системного блока
                self.main_window.ui.invent_num.setText(result[13])  # Инвентарный номер
                self.main_window.ui.IP.setText(result[14])  # IP
                self.main_window.ui.virtual_IP.setText(result[15])  # Виртуальный IP

                self.main_window.ui.office.setText(str(result[16]))  # Номер кабинета
                self.main_window.ui.street.setText(result[17])  # Улица
                self.main_window.ui.house_num.setText(result[18])  # Дом

                # Добавляем данные о технических средствах в таблицу tableWidget
                tech_query = """
                    SELECT Наименование, Марка, [СерийныйНомер]
                    FROM [ТехническиеСредства]
                    WHERE [Код системного блока] = (
                        SELECT [Код системного блока] 
                        FROM [СистемныеБлоки] 
                        WHERE [ИнвентарныйНомер] = ?
                    )
                """
                tech_cursor = self.db_connection.cursor()
                tech_cursor.execute(tech_query, (result[13],))  # Передаем код системного блока
                tech_result = tech_cursor.fetchall()
                print("Результат запроса:", tech_result)

                for row_data in tech_result:
                    row_position = self.main_window.ui.table_tech.rowCount()
                    self.main_window.ui.table_tech.insertRow(row_position)
                    for col_num, col_data in enumerate(row_data):
                        self.main_window.ui.table_tech.setItem(row_position, col_num,
                                                               QtWidgets.QTableWidgetItem(str(col_data)))

                self.main_window.show()
            else:
                print("Данные не найдены")


class SelectWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.selectMain)
        self.ui.pushButton_2.clicked.connect(self.selectSearch)

    def selectMain(self):
        self.main_window = MainWindow()
        self.main_window.show()

    def selectSearch(self):
        self.search_window = SearchWindow()
        self.search_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SelectWindow()
    window.show()
    sys.exit(app.exec_())