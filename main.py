import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
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

    def add_emp(self):
        data = {
                    "name": self.ui.lineEdit.text(),
                    "surname": self.ui.lineEdit_2.text(),
                    "patronymic": self.ui.lineEdit_3.text()
                }
        print(data)

    def delete_emp(self):
        pass

    def update_emp(self):
        data = {
            "name": self.ui.lineEdit.text(),
            "surname": self.ui.lineEdit_2.text(),
            "patronymic": self.ui.lineEdit_3.text()
        }
        print(data)

    def search_emp(self):

        data = {
            "name": self.ui.lineEdit.text(),
            "surname": self.ui.lineEdit_2.text(),
            "patronymic": self.ui.lineEdit_3.text()
        }

        print(data)





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
