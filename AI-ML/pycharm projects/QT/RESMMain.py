import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

from RESM import Ui_MainWindow


class demomain(QMainWindow,Ui_MainWindow):
    def __init__(self,parent= None,):
        super(demomain,self).__init__(parent)
        self.setupUi(self)

        self.PB_System.clicked.connect(lambda :self.stackedWidget.setCurrentWidget(self.SW_System))
        self.PB_SubSystem.clicked.connect(lambda :self.stackedWidget.setCurrentWidget(self.SW_SubSystem))
        self.PB_Calibration.clicked.connect(lambda :self.stackedWidget.setCurrentWidget(self.SW_Calibration))
        self.PB_Settings.clicked.connect(lambda :self.stackedWidget.setCurrentWidget(self.SW_Settings))
        self.PB_Reports.clicked.connect(lambda :self.stackedWidget.setCurrentWidget(self.SW_Reports))




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = demomain()
    win.show()
    sys.exit(app.exec_())