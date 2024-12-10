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




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
