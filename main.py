import sys
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

######## Data Base Connection ########
import mysql.connector


########### welcome.ui #########

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcome_screen.ui",self)
        self.addimage()
        self.Signup.clicked.connect(self.signup)
        self.Login.clicked.connect(self.login)

    def addimage(self):
        qp=QPixmap("blur.jpg")
        self.label.setPixmap(qp)

    def login(self):
        user=self.username.text()
        pwd=self.password.text()
        if len(user)==0 or len(pwd)==0:
            self.error.setText("Incorrect credentials")
        else:
            try:
                # connecting to DB and validating the Uname and pwd
                mydb = mysql.connector.connect(
                    host='localhost',
                    user='Mysql user',
                    passwd='Enter Your password',
                    port='Your default port',
                    database='test')
                cur=mydb.cursor()
                cur.execute('SELECT * from account_details where Username=%s and Password=%s'
                       ,(user,pwd))
                if cur.fetchone():
                    self.error.setText("successfull")
                    obj = DashBoard()
                    widget.addWidget(obj)
                    widget.setCurrentIndex(widget.currentIndex() + 1)

                else:
                    self.error.setText("Incorrect credentials or Pwd")
            except Exception as es:
                print("Error")


    def signup(self):
        obj = SignUp()
        widget.addWidget(obj)
        widget.setCurrentIndex(widget.currentIndex() + 1)




########### Dashboard.ui #########

class DashBoard(QDialog):
    def __init__(self):
        super(DashBoard, self).__init__()
        loadUi("DashBoard.ui",self)
        self.addimage()
        self.Exit.clicked.connect(self.exit)

    def addimage(self):
        qp = QPixmap("blur.jpg")
        self.label.setPixmap(qp)

    def exit(self):
        obj=WelcomeScreen()
        widget.addWidget(obj)
        widget.setCurrentIndex(widget.currentIndex()+1)


########### signup.ui #########

class SignUp(QDialog):
    def __init__(self):
        super(SignUp, self).__init__()
        loadUi("Sign_Up.ui", self)
        self.addimage()
        self.Signup_2.clicked.connect(self.goback)
        self.Signup.clicked.connect(self.signup)

    def addimage(self):
        qp = QPixmap("blur.jpg")
        self.label.setPixmap(qp)

    def goback(self):
        obj=WelcomeScreen()
        widget.addWidget(obj)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def signup(self):
        name = self.name.text()
        Phnum = self.phnum.text()
        pwd = self.password.text()
        user = self.username.text()
        confirmpwd = self.confirmPassword.text()
        if (len(name) and len(Phnum) and len(pwd) and len(user)
            and len(confirmpwd)) == 0:
            self.error.setText("Please fill all Credentials")
        else:
            if pwd == confirmpwd:
                try:
                    mydb = mysql.connector.connect(
                        host='localhost',
                        user='root',
                        passwd='kumar',
                        port='3306',
                        database='test')
                    cur = mydb.cursor()
                    id_query="SELECT max(id) from test.account_details"
                    cur.execute(id_query)
                    R=cur.fetchone()
                    if R!=None and R[0]!=None:
                        id=int(R[0])+1
                    cur = mydb.cursor()
                    sql="insert into test.account_details(id,Name,PhNum,Username,Password) values(%s, %s, %s, %s, %s)"
                    cur.execute(sql,(id,name,Phnum,user,pwd))
                    mydb.commit()
                    if cur.fetchone():
                        self.error.setText("ERROR")
                    else:
                         self.error.setText("Sign Up Successfull ")
                         self.error.setStyleSheet("color:green")
                         self.error.setFont(QFont('MS Shell Dlg 2', 14))

                except Exception as es:
                    print("error")
                    self.error.setText("ERROR ")
            else:
                self.error.setText("Passwords don't match")


########### MAIN CODE #########
#The code below are mandatory to launch the PyQt APP

app = QApplication(sys.argv)
welcome= WelcomeScreen()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(875)
widget.setFixedWidth(1125)
widget.show()
try:
    sys.exit((app.exec()))
except:
    print("exiting")








