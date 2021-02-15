from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import constant
from maingui import mainWindow
import sys 
import os 


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setUi()
        self.w = None
    def setUi(self):
        self.ana_Ayarlar()
        self.layer1()
        

    def ana_Ayarlar(self):
        
        
        self.setWindowTitle('Login')
        self.setGeometry(550,150,400,700)
        self.setFixedSize(400,700)

    def layer1(self):
        image = QLabel(self)
        image.setPixmap(QPixmap('loginImg.png'))
        image.setGeometry(100,50,200,200)
        image.show()

        labelUsername = QLabel('Username',self)
        labelUsername.move(80,300)
        labelPass = QLabel('Password',self)
        labelPass.move(80,350)

        self.txtboxUsername = QLineEdit(self)
        self.txtboxUsername.move(150,300)
        self.txtboxUsername.resize(150,30)

        self.txtboxPassword = QLineEdit(self)
        self.txtboxPassword.setEchoMode(QLineEdit.Password)
        self.txtboxPassword.move(150,350)
        self.txtboxPassword.resize(150,30)

        self.txtboxUsername.setPlaceholderText('username')
        self.txtboxPassword.setPlaceholderText('password')

        loginButton = QPushButton('Login',self)
        loginButton.move(150,400)
        loginButton.resize(100,30)
        loginButton.clicked.connect(self.lgnButtonEvent)

        
        


    def hataDialog(self,strErr):
        errBox = QMessageBox(self)
        errBox.setStyleSheet("QLabel{min-width: 200px;}");
        errLabel = QLabel(errBox)
        errLabel.setText('Hata ! , ' + strErr)
        errLabel.setAlignment(Qt.AlignCenter)
        errBox.exec()
    def lgnButtonEvent(self):
        if self.txtboxUsername.text() == constant.USERNAME  and self.txtboxPassword.text() == constant.PASSWORD :
            if self.w is None:
                
                self.close()
                self.w = mainWindow()
                self.w.show()
        else : 
            self.hataDialog('Giris Basarisiz.')
        

if __name__ == '__main__' :
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('login.png'))
    w = LoginWindow()
    w.show()
    app.exec_()
