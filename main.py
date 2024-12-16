import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

from Presenter import presenter
from main_window import Ui_MainWindow as Ui_MainWindow3

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icons/icon_window.png"))
        self.ui = Ui_MainWindow3()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.ui.add_button.clicked.connect(self.add_emp)
        self.ui.delete_button.clicked.connect(self.delete_emp)
        self.ui.search_buttoin.clicked.connect(self.search_emp)
        self.ui.update_button.clicked.connect(self.update_emp)
        self.ui.tableWidget.itemClicked.connect(self.handle_table_item_click)
        self.presenter = presenter
        self.selected_row = None

    def add_emp(self):
        data = self.get_attributes()
        self.presenter.add_employee(data=data)
        QMessageBox.information(self, "Успех", "Запись добавлена!")
        self.clear()

    def delete_emp(self) -> None:
        flag = self.check_before_delete()
        if flag is True:
            self.presenter.delete_employee(self.id)
            QMessageBox.information(self, "Успех", "Запись удалена!")


    def update_emp(self):
        data = self.get_attributes()
        self.presenter.update_employee(data)
        QMessageBox.information(self, "Успех", "Запись обновлена!")
        self.clear()

    def search_emp(self):
        self.ui.tableWidget.setRowCount(0)
        result = self.presenter.get_all_employees()

        for row_num, row_data in enumerate(result):
            self.ui.tableWidget.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                print(col_data)
                self.ui.tableWidget.setItem(row_num, col_num,QtWidgets.QTableWidgetItem(str(col_data[1])))

        self.clear()


    def get_attributes(self):
        data = {
            "name": self.ui.lineEdit_2.text(),
            "surname": self.ui.lineEdit.text(),
            "patronymic": self.ui.lineEdit_3.text()
        }
        return data

    def clear(self):
        self.ui.lineEdit_2.setText("")
        self.ui.lineEdit.setText("")
        self.ui.lineEdit_3.setText("")

    def handle_table_item_click(self, item):
        self.selected_row = item.row()
        self.id = int(self.ui.tableWidget.item(self.selected_row, 0).text())

    def check_before_delete(self):
        if self.selected_row is not None:
            reply = QMessageBox.question(
                self, "Подтверждение удаления",
                "Вы хотите удалить эту запись?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.ui.tableWidget.removeRow(self.selected_row)
                self.selected_row = None
                return True
        else:
            QMessageBox.warning(self, "Предупреждение", "Выберите запись для удаления.")






if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
