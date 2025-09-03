import sys

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from Src.Common.Login import Ui_Dialog
from Src.UserManagement.UserManagement import UserManagement
from Src.Common.constants import *
from pathlib import Path
from PyQt5 import QtCore
from Src.Common.AESCripto import *
#######################################################################################################################
class LoginDlg(QDialog, Ui_Dialog):
    login_signal_dict = QtCore.pyqtSignal(dict)
    def __init__(self, parent=None,):
        super(LoginDlg, self).__init__(parent)
        self.setupUi(self)
        self.filepath = ''
        self.key = "PlatinumTechnologies-Hyderabad"  # Use a strong key for production
        self.PB_SubmitLogin.clicked.connect(self.ValidateLoginCredentials)
        self.PB_Register.clicked.connect(lambda: self.SW_LOGIN_Page.setCurrentWidget(self.SW_Register))
        self.PB_Reset_Back.clicked.connect(lambda: self.SW_LOGIN_Page.setCurrentWidget(self.SW_Notregister))
        self.PB_DeleteUser.clicked.connect(self.DeleteUserInit)

        self.PB_ModifyAccessLevel.clicked.connect(self.ModifyAccessLevelInit)
        self.CB_Modify_UserName.currentTextChanged.connect(self.ModifyAccUpdatePreAccLev)
        self.PB_Register_Back.clicked.connect(lambda: self.SW_LOGIN_Page.setCurrentWidget(self.SW_Notregister))
        self.PB_DeleteUser_Back.clicked.connect(lambda: self.SW_LOGIN_Page.setCurrentWidget(self.SW_Notregister))
        self.PB_Modify_Back.clicked.connect(lambda: self.SW_LOGIN_Page.setCurrentWidget(self.SW_Notregister))
        self.PB_Modify_Ok.clicked.connect(self.ModifyAccessLevel)
        self.PB_DeleteUser_Delete.clicked.connect(self.DeleteUserCredentials)

        # self.CB_UserName.currentIndexChanged.connect(
        #     lambda: self.CB_PresentAccessLevel.setItemText('Hello'))
        self.PB_Create.clicked.connect(self.RegisterUser)
        self.PB_Reset_Ok.clicked.connect(self.ResetPassword)

        # Connect the label click event to the slot method
        self.label_ForgotPassword.mouseReleaseEvent = self.on_forgot_password_clicked

        # Show/hide passwords
        self.showHideLoginPass.clicked.connect(lambda: self.showHideLoginPassword())
        self.show_hide_signup_password.clicked.connect(lambda: self.showHideSignupPassword())
        self.show_hide_signup_conf_password.clicked.connect(lambda: self.showHideSignupConfPassword())
        self.show_hide_Reset_password.clicked.connect(lambda:self.showHideResetForgotPassword())
        self.show_hide_Reset_conf_password.clicked.connect(lambda: self.showHideResetConfForgotPassword())
        self.CB_Accesslevel.addItems(['Admin','Exec','View'])
    ###############################################################################################################
    def DeleteUserInit(self):
        self.CB_DeleteUser_UserNames.clear()
        self.CB_DeleteUser_UserNames.addItems(self.um.usrmgnt['passwords'].keys())
        self.SW_LOGIN_Page.setCurrentWidget(self.SW_DeleteUser)
    ###############################################################################################################
    def DeleteUserCredentials(self):
        reply = QMessageBox.warning(self,'Login','Are you sure to Delete?',QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            username = self.CB_DeleteUser_UserNames.currentText()
            self.um.DeleteUser(username=username)
            self.CB_DeleteUser_UserNames.clear()
            self.CB_DeleteUser_UserNames.addItems(self.um.usrmgnt['passwords'].keys())
            self.SaveLoginData()
            print(self.um.usrmgnt)
            QMessageBox.information(self, 'Login', f''' '{username}' Deleted''')
    ###############################################################################################################
    def ModifyAccessLevelInit(self):
        self.CB_Modify_UserName.clear()
        self.CB_Modify_UserName.addItems(self.um.usrmgnt['accesslevel'].keys())
        self.SW_LOGIN_Page.setCurrentWidget(self.SW_ModifyAccessLevel)
    ###############################################################################################################
    def ModifyAccessLevel(self):
        username =self.CB_Modify_UserName.currentText()
        accesslevel = self.CB_Modify_PresentAccessLevel.currentText()
        self.um.ModifyAccessLevel(username=username,accesslevel=accesslevel)
        self.SaveLoginData()
        print(self.um.usrmgnt)
        QMessageBox.information(self, 'Login', f'''Access Level of '{username}' Modified to {accesslevel}''')
    ###############################################################################################################
    def ModifyAccUpdatePreAccLev(self):
        username =self.CB_Modify_UserName.currentText()
        self.label_Modify_NewAccessLevel.setText(self.um.usrmgnt['accesslevel'][username])
    ###############################################################################################################
    def on_forgot_password_clicked(self, event):
        self.CB_Reset_UserName.clear()
        self.CB_Reset_UserName.addItems(self.um.usrmgnt['passwords'].keys())
        self.SW_LOGIN_Page.setCurrentWidget(self.SW_ResetPassword)
    ###############################################################################################################
    def ResetPassword(self):
        print('Reset Password')
        reset_password = self.Reset_password.text()
        con_reset_password = self.Reset_conf_password.text()
        if reset_password == con_reset_password :
            self.um.ModifyPassword(username=self.CB_Reset_UserName.currentText(),newpassword=reset_password)
            self.SaveLoginData()
            print(self.um.usrmgnt)
    ###############################################################################################################
    def RegisterUser(self):
        print('Register User')
        username = self.signup_username.text()
        password = self.signup_password.text()
        con_password = self.signup_conf_password.text()
        if username == '':
            QMessageBox.warning(self,'Login', 'username filed empty!!!')
        else:
            Status = self.um.ValidateCredentials(username=username)['errorcode']
            if Status == INCORRECT_PASSWORD:
                QMessageBox.critical(self, 'Login', f'''username - '{username}' already Exists''')
            if Status == INCORRECT_USERNAME:
                if password == con_password:
                    self.um.AddNewUser(username=username,password=password,accesslevel=self.CB_Accesslevel.currentText())
                    self.SaveLoginData()
                    QMessageBox.information(self, 'Login', f'''New user '{username}' Created''')
                else:
                    QMessageBox.warning(self, 'Login', f'password & con_password mismatch!!!')
    ###############################################################################################################
    def ValidateLoginCredentials(self):
        print('Login Button Clicked')
        username = self.loginUsername.text()
        password = self.loginPassword.text()
        self.um = UserManagement()

        filename = f'{self.filepath}/LoginData.aes'
        try:
            userdata = Path(filename).read_text()
            # print(userdata)
            decrypted = decrypt_json(userdata, self.key)
            # self.um.passwords = decrypted['passwords']
            # self.um.accesslevel = decrypted['accesslevel']
        except:
            QMessageBox.warning(self,'Login', 'Unable to Read\n' + filename)
            return
        #print(um.passwords)
        self.um.usrmgnt = {
            'passwords': decrypted['passwords'],
            'accesslevel' : decrypted['accesslevel']
        }
        status = self.um.ValidateCredentials(username, password)
        if status['errorcode'] == INCORRECT_USERNAME:
            QMessageBox.warning(self,'Login', 'Invalid User Name')
        elif status['errorcode'] == INCORRECT_PASSWORD:
            QMessageBox.warning(self,'Login', 'Incorrect Password')
        else:
            access_level = self.um.GetAccessLevel(username=username)['accesslevel']
            print(access_level)
            self.login_signal_dict.emit({'function':'login','username':username,'accesslevel':access_level})
    ###############################################################################################################
    def showHideSignupPassword(self):
        if self.signup_password.echoMode() == QLineEdit.EchoMode.Password:
            # Change Icon
            eyeIcon = QIcon()
            eyeIcon.addFile(":/icons/Resource/icons/eye_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
            self.show_hide_signup_password.setIcon(eyeIcon)
            # Change echo mode
            self.signup_password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            # change icon
            eyeIcon = QIcon()
            eyeIcon.addFile(":/icons/Resource/icons/eye-off_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
            self.show_hide_signup_password.setIcon(eyeIcon)
            # Change echo mode
            self.signup_password.setEchoMode(QLineEdit.EchoMode.Password)
    ###############################################################################################################
    def showHideSignupConfPassword(self):
        if self.signup_conf_password.echoMode() == QLineEdit.EchoMode.Password:
            # Change Icon
            eyeIcon = QIcon()
            eyeIcon.addFile(":/icons/Resource/icons/eye_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
            self.show_hide_signup_conf_password.setIcon(eyeIcon)
            # Change echo mode
            self.signup_conf_password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            # change icon
            eyeIcon = QIcon()
            eyeIcon.addFile(":/icons/Resource/icons/eye-off_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
            self.show_hide_signup_conf_password.setIcon(eyeIcon)
            # Change echo mode
            self.signup_conf_password.setEchoMode(QLineEdit.EchoMode.Password)
    ###############################################################################################################
    def showHideLoginPassword(self):
        if self.loginPassword.echoMode() == QLineEdit.EchoMode.Password:
            # Change Icon
            eyeIcon = QIcon()
            eyeIcon.addFile(":/icons/Resource/icons/eye_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
            self.showHideLoginPass.setIcon(eyeIcon)
            # Change echo mode
            self.loginPassword.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            # change icon
            eyeIcon = QIcon()
            eyeIcon.addFile(":/icons/Resource/icons/eye-off_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
            self.showHideLoginPass.setIcon(eyeIcon)
            # Change echo mode
            self.loginPassword.setEchoMode(QLineEdit.EchoMode.Password)
    ###############################################################################################################
    def showHideResetForgotPassword(self):
        if self.Reset_password.echoMode() == QLineEdit.EchoMode.Password:
            # Change Icon
            eyeIcon = QIcon()
            eyeIcon.addFile(":/icons/Resource/icons/eye_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
            self.show_hide_Reset_password.setIcon(eyeIcon)
            # Change echo mode
            self.Reset_password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            # change icon
            eyeIcon = QIcon()
            eyeIcon.addFile(":/icons/Resource/icons/eye-off_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
            self.show_hide_Reset_password.setIcon(eyeIcon)
            # Change echo mode
            self.Reset_password.setEchoMode(QLineEdit.EchoMode.Password)
    ###############################################################################################################
    def showHideResetConfForgotPassword(self):
        if self.Reset_conf_password.echoMode() == QLineEdit.EchoMode.Password:
            # Change Icon
            eyeIcon = QIcon()
            eyeIcon.addFile(":/icons/Resource/icons/eye_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
            self.show_hide_Reset_conf_password.setIcon(eyeIcon)
            # Change echo mode
            self.Reset_conf_password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            # change icon
            eyeIcon = QIcon()
            eyeIcon.addFile(":/icons/Resource/icons/eye-off_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
            self.show_hide_Reset_conf_password.setIcon(eyeIcon)
            # Change echo mode
            self.Reset_conf_password.setEchoMode(QLineEdit.EchoMode.Password)
    ###############################################################################################################
    def SaveLoginData(self):
        encrypted = encrypt_json(self.um.usrmgnt, self.key)
        print("Encrypted:", encrypted)
        filename = f'{self.filepath}/LoginData.aes'
        print(filename)
        print(self.um.usrmgnt)
        text_file = open(filename, "w")
        text_file.write(encrypted)
########################################################################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginDlg()
    # win.State = 'login'
    win.show()
    sys.exit(app.exec_())

