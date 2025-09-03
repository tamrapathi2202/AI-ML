import sys
from platform import system

from PyQt5.QtWidgets import QMainWindow, QApplication

from system import Ui_MainWindow


class systemmain(QMainWindow,Ui_MainWindow):
    def __init__(self,parent= None,):
        super(systemmain,self).__init__(parent)
        self.setupUi(self)








if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = systemmain()
    win.show()
    sys.exit(app.exec_())