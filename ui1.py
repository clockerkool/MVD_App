from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(242, 103)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Comfortaa")
        font.setPointSize(12)
        self.listWidget.setFont(font)
        self.listWidget.setStyleSheet("QListWidget::item { \n"
" background-color: rgba(10, 116, 240, 255);\n"
" color: white;\n"
" border:none;\n"
"}\n"
"\n"
"\n"
"QListWidget\n"
"{\n"
" color: black;\n"
" border:none; \n"
"}\n"
"\n"
"\n"
"QScrollBar::handle:vertical\n"
"{\n"
" Background: rgba(10, 116, 240, 160);\n"
" Border: 0px solid grey;\n"
" Border-radius: 3px; \n"
" Width: 8px;\n"
"}\n"
"\n"
"\n"
"")
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.horizontalLayout.addWidget(self.listWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Операционные сисетмы"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "Windows 7"))
        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", "Windows 10"))
        item = self.listWidget.item(2)
        item.setText(_translate("MainWindow", "Windows 11"))
        item = self.listWidget.item(3)
        item.setText(_translate("MainWindow", "Astra Linux"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
