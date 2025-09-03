from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
import sys
from DIFM import Ui_MainWindow


class DIFMmain(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(DIFMmain, self).__init__(parent)
        self.setupUi(self)
        self.PB_Save.clicked.connect(self.Save)
        self.PB_Print.clicked.connect(self.Print)
        self.PB_Settings.clicked.connect(self.Settings)
        self.PB_Start.clicked.connect(self.Start)
    def Save(self):
        print("save clicked")
    def Print(self):
        print("print clicked")
    def Settings(self):
        print("setting clicked")
    def Start(self):
        print("Start clicked")


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    #MainWindow = QtWidgets.QMainWindow()
    ui = DIFMmain()
    ui.show()
    sys.exit(app.exec_())
