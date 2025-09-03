import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

from RadiationMode import Ui_MainWindow


class RadiationModeMain(QMainWindow,Ui_MainWindow):
    def __init__(self,parent= None,):
        super(RadiationModeMain,self).__init__(parent)
        self.setupUi(self)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = RadiationModeMain()
    win.show()
    sys.exit(app.exec_())