import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

from demo import Ui_MainWindow


class demomain(QMainWindow,Ui_MainWindow):
    def __init__(self,parent= None,):
        super(demomain,self).__init__(parent)
        self.setupUi(self)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = demomain()
    win.show()
    sys.exit(app.exec_())