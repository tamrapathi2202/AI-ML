from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
import sys
from CreateDatabase import Ui_MainWindow


class CreateDatabaseMain(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(CreateDatabaseMain,self).__init__(parent)
        self.setupUi(self)
        self.PB_Connect.clicked.connect(self.connect)
        self.PB_Close.clicked.connect(self.close)
        self.PB_Create.clicked.connect(self.create)
    def connect(self):
        print("connection clicked")
    def close(self):
        print("connection closed")
    def create(self):
        print("connection created")


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    ui = CreateDatabaseMain()
    ui.show()
    sys.exit(app.exec_())


