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
        self.presenter = presenter
        self.ui.add_button.clicked.connect(self.add_emp)
        self.ui.delete_button.clicked.connect(self.delete_emp)
        self.ui.search_buttoin.clicked.connect(self.search_emp)
        self.ui.update_button.clicked.connect(self.update_emp)

    def add_emp(self):
        data = self.get_attributes()
        self.presenter.add_employee(data=data)
        QMessageBox.information(self, "Успех", "Запись добавлена!")
        self.clear()

    def delete_emp(self):
        QMessageBox.information(self, "Успех", "Запись удалена!")

    def update_emp(self):
        data = self.get_attributes()
        QMessageBox.information(self, "Успех", "Запись обновлена!")
        self.clear()

    def search_emp(self):
        data = self.get_attributes()
        self.presenter.get_all_employees()
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





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
