import sys
import pyodbc
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
from WordDocx import *
from ExcelGen import *
from GenerateDocuments import RequestFileCreator, TechDevicesFileCreator
import ui3
from DB_functions import *
#from ui import Ui_MainWindow as Ui_MainWindow2
from ui1 import Ui_MainWindow as Ui_MainWindow1
from untitled2 import Ui_MainWindow as Ui_MainWindow3
from ui3 import Ui_MainWindow as Ui_MainWindow
from final_interface import Ui_MainWindow as Ui_MainWindow2
from datetime import datetime
from PIL import Image

import io

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icons/icon_window.png"))
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
        self.ui.get_docx.clicked.connect(self.return_docx)
        self.ui.attach_passport.clicked.connect(self.open_file_dialog)
        self.ui.table_os.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.update_button_positions()

    def get_user_data(self):
        """Получение, введённых пользователем, данных"""
        self.kab = int(self.ui.office.text())
        self.street = self.ui.street.text()
        self.home = self.ui.house_num.text()
        self.surname = self.ui.surname.text()
        self.name = self.ui.name.text()
        self.patronymic = self.ui.patronymic.text()
        self.birthday = self.ui.born_date.text()
        self.gender = "M" if self.ui.gender_M.isChecked() else "Ж"
        self.post = self.ui.post.text()
        self.rank = self.ui.rank.text()
        self.division = self.ui.division.text()
        self.region = self.ui.region.text()
        self.phone_number = self.ui.phone_number.text()
        self.SNILS = self.ui.snils.text()
        self.model = self.ui.model.text()
        self.invent_num = self.ui.invent_num.text()
        self.IP = self.ui.IP.text()
        self.virtual_IP = self.ui.virtual_IP.text()
        self.kab_code = get_id_kab()
        self.os = ""
        for row in range(self.ui.table_os.rowCount()):
            for column in range(self.ui.table_os.columnCount()):
                item = self.ui.table_os.item(row, column)
                if item is not None:
                    self.os += item.text() + "; "

    def add_data(self):
        """Добавление данных в БД"""
        try:
            if self.check_fields() is False:
                QMessageBox.information(self, "Внимание!", "Не все поля заполнены, либо заполнены некорректно!")
                return
            self.get_user_data()
            self.temp_id = SearchWindow().id
            print("ID_TO_UPDATE: ", self.temp_id)
            if self.temp_id != None:
                self.update_data()
                return
            insert_to_kab(self.kab, self.street, self.home)
            insert_to_employee(self.surname, self.name, self.patronymic, self.birthday,
                               self.gender, self.post, self.rank, self.division, self.region,
                               self.phone_number,self.SNILS)
            self.emp_code = get_id_emp()
            insert_to_sys_unit(self.model, self.invent_num, self.IP, self.virtual_IP, self.kab_code, self.emp_code)
            self.add_os()
            self.add_tech()
        except:
            QMessageBox.information(self, "Внимание!", "Что-то пошло не так!")



    def update_data(self):
        try:
            if self.check_fields() is False:
                QMessageBox.information(self, "Внимание!", "Не все поля заполнены, либо заполнены некорректно!")
                return
            update_emp(self.temp_id, self.surname, self.name, self.patronymic, self.birthday,
                       self.gender, self.post, self.rank, self.division, self.region, self.phone_number, self.SNILS)
            update_sys_unit(self.model, self.invent_num, self.IP, self.virtual_IP, self.temp_id)
            update_kab(self.temp_id, self.kab, self.street, self.home)

            ###
            os = ""
            for row in range(self.ui.table_os.rowCount()):
                for column in range(self.ui.table_os.columnCount()):
                    item = self.ui.table_os.item(row, column)
                    if item is not None:
                        os += item.text() + "; "
            update_os(self.temp_id, os)


            table_values = []
            for row in range(self.ui.table_tech.rowCount()):
                row_values = []
                for column in range(self.ui.table_tech.columnCount()):
                    item = self.ui.table_tech.item(row, column)
                    if item is not None:
                        row_values.append(item.text())
                    else:
                        row_values.append("")  # Если ячейка пуста, добавляем пустую строку
                table_values.append(row_values)
            update_tech(self.temp_id, table_values)
            SearchWindow.id = None
        except:
            QMessageBox.information(self, "Что-то пошло не так!")

    def add_os(self):
        """"Функция для записи OS в БД"""
        insert_to_os(self.os)


    def add_tech(self):
        """Функция для записи Технических средств в БД"""
        table_values = []
        for row in range(self.ui.table_tech.rowCount()):
            row_values = []
            for column in range(self.ui.table_tech.columnCount()):
                item = self.ui.table_tech.item(row, column)
                if item is not None:
                    row_values.append(item.text())
                else:
                    row_values.append("")  # Если ячейка пуста, добавляем пустую строку
            table_values.append(row_values)
            print(table_values)
        inset_to_tech(table_values)


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


    def return_docx(self):
        self.get_user_data()
        RequestFileCreator().create().generate_file(f"{self.surname} {self.name[0]}.{self.patronymic[0]}")
        TechDevicesFileCreator().create().generate_file(self.transform_tech_data())
        get_list1([self.surname, self.name, self.patronymic, self.birthday, self.gender, self.post, self.rank, self.division,
                   self.region, self.kab, self.phone_number, "49-49-49", self.SNILS])
        get_exel(["1", self.IP, self.virtual_IP, "инсппектор отдела статистики, Петров П.П."])
        get_exel4([self.os, self.invent_num, f'г.Курган {self.street} {self.home}', self.kab, self.post,
                   f"{self.surname} {self.name} {self.patronymic}", self.phone_number])

    def transform_tech_data(self):
        data = []

        # Проходим по всем строкам TableWidget
        for row in range(self.ui.table_tech.rowCount()):
            row_data = {}
            # Проходим по всем столбцам в строке
            for col in range(self.ui.table_tech.columnCount()):
                # Получаем значение ячейки
                item = self.ui.table_tech.item(row, col)
                if item:
                    # Добавляем значение в словарь с соответствующим ключом
                    row_data[f'col_{col + 1}'] = item.text()
            # Добавляем словарь строки в общий список данных
            row_data[f'col_4'] = self.street + " " + self.home
            row_data[f'col_5'] = self.kab
            data.append(row_data)

        # Переименование ключей в словаре
        for item in data:
            item['name_sys'] = item.pop('col_1')
            item['model_sys'] = item.pop('col_2')
            item['id_sys'] = item.pop('col_3')
            item['address'] = item.pop('col_4')
            item['office_num'] = item.pop('col_5')
        return data


    def handle_os_item_click(self, item):
        selected_os = item.text()
        row_count = self.ui.table_os.rowCount()
        self.ui.table_os.insertRow(row_count)
        self.ui.table_os.setItem(row_count, 0, QtWidgets.QTableWidgetItem(selected_os))
        # Обновляем значение выбранного инвентарного номера при выборе операционной системы
        self.selected_inventory_number = selected_os

    def open_file_dialog(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Открыть изображение", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.load_and_save_image(file_name)

    def load_and_save_image(self, file_path):
        try:
            with open(file_path, "rb") as image_file:
                image_data = image_file.read()
            # Преобразуем данные изображения в формат, подходящий для Access
            # (двоичные данные в виде массива байтов)
            image_data = bytearray(image_data)
        except Exception as e:
            print(f"Ошибка при загрузке и сохранении изображения: {e}")


    def check_fields(self):
        flag = True
        try:
            #print(int(self.ui.office.text()))
            if int(self.ui.office.text()) and len(self.ui.office.text()) == 0:
                flag = False
            elif len(self.ui.street.text()) == 0:
                flag = False
            elif int(self.ui.house_num.text()) and len(self.ui.house_num.text()) == 0:
                flag = False
            elif len(self.ui.surname.text()) == 0:
                flag = False
            elif  len(self.ui.name.text()) == 0:
                flag = False
            elif  len(self.ui.patronymic.text()) == 0:
                flag = False
            elif  len(self.ui.born_date.text()) == 0:
                flag = False
            elif  not self.ui.gender_M.isChecked() and  not self.ui.gender_W.isChecked():
                flag = False
            elif len(self.ui.post.text()) == 0:
                flag = False
            elif  len(self.ui.rank.text()) == 0:
                flag = False
            elif  len(self.ui.division.text()) == 0:
                flag = False
            elif len(self.ui.region.text()) == 0:
                flag = False
            elif  len(self.ui.phone_number.text()) == 0:
                flag = False
            elif len(self.ui.snils.text()) == 0:
                flag = False
            elif  len(self.ui.model.text()) == 0:
                flag = False
            elif  len(self.ui.invent_num.text()) == 0:
                flag = False
            elif  len(self.ui.IP.text()) == 0:
                flag = False
            elif  len(self.ui.virtual_IP.text()) == 0:
                flag = False
            elif self.ui.table_os.rowCount() == 0:
                flag = False
            elif self.ui.table_tech.rowCount() == 0:
                flag = False
            return flag
        except:
            print("Что-то не так в вводе")
            return False





class OSWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow1()
        self.setWindowIcon(QIcon("icons/icon_window.png"))
        self.ui.setupUi(self)


class SearchWindow(QtWidgets.QMainWindow):
    id = None
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SearchWindow, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow3()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.search)
        self.ui.pushButton_2.clicked.connect(self.open_main_window)
        self.setFixedSize(self.size())
        self.ui.tableWidget.setColumnWidth(0, 45)
        self.ui.tableWidget.setColumnWidth(1, 140)
        self.ui.tableWidget.setColumnWidth(2, 140)
        self.ui.tableWidget.setColumnWidth(3, 150)
        self.ui.tableWidget.setColumnWidth(4, 140)
        self.ui.tableWidget.setColumnWidth(5, 235)
        self.ui.pushButton_3.clicked.connect(self.delete_record)
        self.selected_row = None
        self.setWindowIcon(QIcon("icons/icon_window.png"))
        self.db_connection = pyodbc.connect(
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + get_db_path() + ';'
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
        #print(result)
        self.ui.tableWidget.setRowCount(0)

        for row_num, row_data in enumerate(result):
            self.ui.tableWidget.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                self.ui.tableWidget.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(str(col_data)))

    # Обработчик событий для таблицы
    def handle_table_item_click(self, item):
        self.selected_row = item.row()
        print("SW:", self.ui.tableWidget.item(self.selected_row, 0).text())
        SearchWindow.id = self.ui.tableWidget.item(self.selected_row, 0).text()
        self.selected_inventory_number = self.ui.tableWidget.item(self.selected_row, 5).text()
        print("Выбранный инвентарный номер:", self.selected_inventory_number)  # Выводим для отладки


    def open_main_window(self):
        self.close()
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
                print('result', result[5], ord(result[5]), ord('М'), len(result[5]))
                if  ord(result[5]) == 77:
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
                    WHERE [КодСистемногоБлока] = (
                        SELECT [КодСистемногоБлока] 
                        FROM [СистемныеБлоки] 
                        WHERE [ИнвентарныйНомер] = ?
                    )
                """
                tech_cursor = self.db_connection.cursor()
                print(result[13])
                tech_cursor.execute(tech_query, (result[13],))  # Передаем код системного блока
                tech_result = tech_cursor.fetchall()
                print("Результат запроса:", tech_result)

                for row_data in tech_result:
                    row_position = self.main_window.ui.table_tech.rowCount()
                    self.main_window.ui.table_tech.insertRow(row_position)
                    for col_num, col_data in enumerate(row_data):
                        self.main_window.ui.table_tech.setItem(row_position, col_num,
                                                               QtWidgets.QTableWidgetItem(str(col_data)))

                    # Заполнение table_os
                    os_query = """
                                        SELECT Наименование
                                        FROM ОперационныеСистемы
                                        WHERE КодСистемногоБлока = (
                                            SELECT КодСистемногоБлока
                                            FROM СистемныеБлоки
                                            WHERE ИнвентарныйНомер = ?
                                        )
                                    """
                    os_cursor = self.db_connection.cursor()
                    os_cursor.execute(os_query, (self.selected_inventory_number,))
                    os_result = os_cursor.fetchone()
                    print("Результат запроса:", os_result)
                    if os_result:
                        os_list = os_result[0].split('; ')
                        if os_list:
                            for os_name in os_list[:-1]:
                                row_position = self.main_window.ui.table_os.rowCount()
                                self.main_window.ui.table_os.insertRow(row_position)
                                self.main_window.ui.table_os.setItem(row_position, 0,
                                                                     QtWidgets.QTableWidgetItem(os_name))

                self.main_window.show()
            else:
                print("Данные не найдены")

    def get_id_to_update(self):
        return self.id

    def delete_record(self):
        if self.selected_row is not None:
            reply = QMessageBox.question(
                self, "Подтверждение удаления",
                "Вы хотите удалить эту запись?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                try:
                    delete_emp(self.id)

                    self.ui.tableWidget.removeRow(self.selected_row)
                    self.selected_row = None

                    QMessageBox.information(self, "Успех", "Запись удалена!")

                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении: {str(e)}")
        else:
            QMessageBox.warning(self, "Предупреждение", "Выберите запись для удаления.")


class SelectWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.main_window = MainWindow()
        self.search_window = SearchWindow()
        self.setWindowIcon(QIcon("icons/icon_window.png"))
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.selectMain)
        self.ui.pushButton_2.clicked.connect(self.selectSearch)

    def selectMain(self):
        self.main_window.show()
        self.close()

    def selectSearch(self):
        self.search_window.show()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SelectWindow()
    window.show()
    sys.exit(app.exec_())
