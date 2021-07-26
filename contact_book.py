"""
Before run start mariadb service:
systemctl start mariadb
Then create user (here "contact") and two databases(here "contact_db" and "contact_book_db")
After that run contact_book.py
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QMainWindow, QWidget, QTabWidget, QLabel, QPushButton, QVBoxLayout, QTableView, QAbstractItemView
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, pyqtSignal, QItemSelection, pyqtSlot, QSortFilterProxyModel, QRegExp
import mariadb
from datetime import datetime
import sys

class Ui_dialog_Login(object):
    def setupUi(self, Dialog): 
        Dialog.setObjectName("Login")
        Dialog.resize(550, 250)
        
        font = QtGui.QFont()
        font.setPointSize(10)
        
        self.email_lable = QtWidgets.QLabel(Dialog)
        self.email_lable.setGeometry(QtCore.QRect(150, 100, 70, 20))
        self.email_lable.setFont(font)
        self.email_lable.setAlignment(QtCore.Qt.AlignCenter)
        self.email_lable.setObjectName("email_lable")

        self.pass_lable = QtWidgets.QLabel(Dialog)
        self.pass_lable.setGeometry(QtCore.QRect(150, 150, 70, 20))
        self.pass_lable.setFont(font)
        self.pass_lable.setAlignment(QtCore.Qt.AlignCenter)
        self.pass_lable.setObjectName("pass_lable")

        self.email_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.email_lineEdit.setGeometry(QtCore.QRect(250, 100, 100, 20))
        self.email_lineEdit.setObjectName("email_lineEdit")

        self.pass_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.pass_lineEdit.setGeometry(QtCore.QRect(250, 150, 100, 20))
        self.pass_lineEdit.setObjectName("pass_lineEdit")

        f = open('checkbox.txt', 'r')
        line = f.readline()
        f.close()
        connection = mariadb.connection(host='localhost',user='contact', password='12345', database="contact_db")
        cur = connection.cursor()
        cur.execute("SELECT * FROM USERS WHERE USERNAME = '" + line + "'")
        result = cur.fetchall()
        if len(result) > 0:
            for data in result:
                self.email_lineEdit.setText(data[0])
                self.pass_lineEdit.setText(data[2])        
        cur.close()

        self.login_btn = QtWidgets.QPushButton(Dialog)
        self.login_btn.setGeometry(QtCore.QRect(200, 200, 50, 20))
        self.login_btn.setObjectName("login_btn")

        self.login_btn.clicked.connect(self.loginClicked)

        self.signup_btn = QtWidgets.QPushButton(Dialog)
        self.signup_btn.setGeometry(QtCore.QRect(300, 200, 50, 20))
        self.signup_btn.setObjectName("signup_btn")

        self.signup_btn.clicked.connect(self.signupClicked)
        
        self.check_btn = QtWidgets.QCheckBox(Dialog)
        self.check_btn.setGeometry(QtCore.QRect(400, 200, 150, 20))
        self.check_btn.setObjectName("check_btn")
    
        self.check_btn.setChecked(False)
        self.check_btn.stateChanged.connect(self.checkboxChecked)

        self.res_pass_btn = QtWidgets.QPushButton(Dialog)
        self.res_pass_btn.setGeometry(QtCore.QRect(400, 100, 150, 20))
        self.res_pass_btn.setObjectName("rem_pass_btn")

        self.res_pass_btn.clicked.connect(self.resPassClicked)

        self.lable = QtWidgets.QLabel(Dialog)
        self.lable.setGeometry(QtCore.QRect(190, 10, 200, 50))

        font = QtGui.QFont()
        font.setPointSize(18)

        self.lable.setFont(font)
        self.lable.setObjectName("lable")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("login dialog")
        self.email_lable.setText("LOGIN")
        self.pass_lable.setText("PASSWORD")
        self.login_btn.setText("Login")
        self.signup_btn.setText("Sign Up")
        self.lable.setText("Login Form")
        self.check_btn.setText("Remember Me")
        self.res_pass_btn.setText("Reset Password")

    def resPassClicked(self):
        self.reswindow = QDialog()
        self.ui = Ui_dialog_resetpassword()
        self.ui.setupUi(self.reswindow)
        self.reswindow.show()

    def checkboxChecked(self):
        if self.check_btn.isChecked() == True:
            f = open('checkbox.txt', 'w')
            f.write(self.email_lineEdit.text())
            f.close()

    def loginClicked(self): 
        usermail = self.email_lineEdit.text()
        userpass =self.pass_lineEdit.text()

        connection = mariadb.connection(host='localhost',user='contact', password='12345', database="contact_db")
        cur = connection.cursor()
        cur.execute("SELECT * FROM USERS WHERE USERNAME = ? AND PASSWORD = ?", (usermail, userpass))
        result = cur.fetchall()
        if len(result) > 0:
            self.openmainwindow(usermail)
            Dialog.close()        
        else:
            self.showMessageBox("Warning", "Invalid username and password")
        cur.close()

    def showMessageBox(self, title, message):
        self.msgBox = QtWidgets.QMessageBox()
        self.msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        self.msgBox.setWindowTitle(title)
        self.msgBox.setText(message)
        self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msgBox.exec_()    

    def openmainwindow(self, usermail):
        self.qmainwindow = QMainWindow()
        self.mainwindow = Ui_main_window()
        self.mainwindow.setupUi(self.qmainwindow, usermail)
        self.qmainwindow.show()
    
    def openSignUpWindow(self):
        self.signupwindow = QDialog()
        self.ui = Ui_dialog_sign_up()
        self.ui.setupUi(self.signupwindow)
        self.signupwindow.show()

    def signupClicked(self):
        self.openSignUpWindow()

class Ui_dialog_sign_up(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Sign up")
        Dialog.resize(500, 300)
        
        font = QtGui.QFont()
        font.setPointSize(10)

        self.nickname_lable = QtWidgets.QLabel(Dialog)
        self.nickname_lable.setGeometry(QtCore.QRect(150, 80, 70, 20))
        self.nickname_lable.setFont(font)
        self.nickname_lable.setAlignment(QtCore.Qt.AlignCenter)
        self.nickname_lable.setObjectName("nickname_lable")
        
        self.email_lable = QtWidgets.QLabel(Dialog)
        self.email_lable.setGeometry(QtCore.QRect(150, 130, 70, 20))
        self.email_lable.setFont(font)
        self.email_lable.setAlignment(QtCore.Qt.AlignCenter)
        self.email_lable.setObjectName("email_lable")

        self.pass_lable = QtWidgets.QLabel(Dialog)
        self.pass_lable.setGeometry(QtCore.QRect(150, 180, 70, 20))
        self.pass_lable.setFont(font)
        self.pass_lable.setAlignment(QtCore.Qt.AlignCenter)
        self.pass_lable.setObjectName("pass_lable")

        self.nickname_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.nickname_lineEdit.setGeometry(QtCore.QRect(250, 80,  150, 20))
        self.nickname_lineEdit.setObjectName("nickname_lineEdit")

        self.email_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.email_lineEdit.setGeometry(QtCore.QRect(250, 130, 150, 20))
        self.email_lineEdit.setObjectName("email_lineEdit")

        self.pass_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.pass_lineEdit.setGeometry(QtCore.QRect(250, 180, 150, 20))
        self.pass_lineEdit.setObjectName("pass_lineEdit")

        self.signup_btn = QtWidgets.QPushButton(Dialog)
        self.signup_btn.setGeometry(QtCore.QRect(250, 220, 50, 20))
        self.signup_btn.setObjectName("signup_btn")

        self.signup_btn.clicked.connect(self.signupClicked)
        
        self.lable = QtWidgets.QLabel(Dialog)
        self.lable.setGeometry(QtCore.QRect(190, 10, 200, 50))

        font = QtGui.QFont()
        font.setPointSize(18)

        self.lable.setFont(font)
        self.lable.setObjectName("lable")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("sign up dialog")
        self.nickname_lable.setText("NAME")
        self.email_lable.setText("EMAIL")
        self.pass_lable.setText("PASSWORD")
        self.signup_btn.setText("Sign Up")
        self.lable.setText("Sign Up Form")

    def insert_data(self):
        username = self.nickname_lineEdit.text()
        useremail = self.email_lineEdit.text()
        userpassword = self.pass_lineEdit.text()

        connection = mariadb.connection(host='localhost',user='contact', password='12345', database="contact_db")
        cur = connection.cursor()
        cur.execute("INSERT INTO USERS VALUES (?, ?, ?)", (username, useremail, userpassword))
        connection.commit()
        connection.close()

    def createNewContactDB(self, name):
        connection = mariadb.connection(host='localhost',user='contact', password='12345', database="contact_book_db")
        cur = connection.cursor()
        cur.execute("SELECT * FROM information_schema.tables WHERE table_name = '" + name + "'")
        result = cur.fetchone()
        if result == None:
            self.insert_data()
            cur.execute("CREATE TABLE IF NOT EXISTS " + name +  "(NAME TEXT NOT NULL, PHONE TEXT NOT NULL, BIRTH TEXT)")
            self.showMessageBox("Information", "You have successfully registred. Now you can close Sign Up Form window.")
        else:
            self.showMessageBox("Warning", "User with this nickname is already exist!")
        cur.close()
        connection.commit()

    def signupClicked(self):
        self.createNewContactDB(self.nickname_lineEdit.text())
        
    def showMessageBox(self, title, message):
        self.msgBox = QtWidgets.QMessageBox()
        self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
        self.msgBox.setWindowTitle(title)
        self.msgBox.setText(message)
        self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msgBox.exec_() 

class Ui_dialog_resetpassword(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Restore Password")
        Dialog.resize(400, 250)
        
        font = QtGui.QFont()
        font.setPointSize(10)

        self.nickname_lable = QtWidgets.QLabel(Dialog)
        self.nickname_lable.setGeometry(QtCore.QRect(50, 80, 70, 20))
        self.nickname_lable.setFont(font)
        self.nickname_lable.setAlignment(QtCore.Qt.AlignCenter)
        self.nickname_lable.setObjectName("nickname_lable")

        self.nickname_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.nickname_lineEdit.setGeometry(QtCore.QRect(130, 80,  150, 20))
        self.nickname_lineEdit.setObjectName("nickname_lineEdit")

        self.reset_btn = QtWidgets.QPushButton(Dialog)
        self.reset_btn.setGeometry(QtCore.QRect(150, 150, 100, 20))
        self.reset_btn.setObjectName("reset_btn")

        self.reset_btn.clicked.connect(self.resetClicked)
        
        self.lable = QtWidgets.QLabel(Dialog)
        self.lable.setGeometry(QtCore.QRect(100, 10, 200, 50))

        font = QtGui.QFont()
        font.setPointSize(18)

        self.lable.setFont(font)
        self.lable.setObjectName("lable")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("Reset dialog")
        self.nickname_lable.setText("LOGIN")
        self.reset_btn.setText("Reset Password")
        self.lable.setText("Reset Form")
    
    def resetClicked(self):
        username = self.nickname_lineEdit.text()

        connection = mariadb.connection(host='localhost',user='contact', password='12345', database="contact_db")
        cur = connection.cursor()
        cur.execute("SELECT * FROM USERS WHERE USERNAME = '" + username + "'")
        result = cur.fetchone()
        if result == None:
            self.showMessageBox("Warning", "User doesn't exist")
        else:
            self.showMessageBox("Password", "Password:  " + result[2])
        cur.close()
        connection.commit()
        
    
    def showMessageBox(self, title, message):
        self.msgBox = QtWidgets.QMessageBox()
        self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
        self.msgBox.setWindowTitle(title)
        self.msgBox.setText(message)
        self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msgBox.exec_() 

class addContactToBookDialog(object):
    def setupContactUi(self, Dialog, usernick):
        Dialog.setObjectName("Add Contact")
        Dialog.resize(500, 300)
        
        font = QtGui.QFont()
        font.setPointSize(10)

        self.name_lable = QtWidgets.QLabel(Dialog)
        self.name_lable.setGeometry(QtCore.QRect(150, 80, 70, 20))
        self.name_lable.setFont(font)
        self.name_lable.setAlignment(QtCore.Qt.AlignCenter)
        self.name_lable.setObjectName("name_lable")
        
        self.phone_lable = QtWidgets.QLabel(Dialog)
        self.phone_lable.setGeometry(QtCore.QRect(150, 130, 70, 20))
        self.phone_lable.setFont(font)
        self.phone_lable.setAlignment(QtCore.Qt.AlignCenter)
        self.phone_lable.setObjectName("phone_lable")

        self.birth_lable = QtWidgets.QLabel(Dialog)
        self.birth_lable.setGeometry(QtCore.QRect(150, 180, 70, 20))
        self.birth_lable.setFont(font)
        self.birth_lable.setAlignment(QtCore.Qt.AlignCenter)
        self.birth_lable.setObjectName("birth_lable")

        self.name_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.name_lineEdit.setGeometry(QtCore.QRect(250, 80,  150, 20))
        self.name_lineEdit.setObjectName("name_lineEdit")

        self.phone_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.phone_lineEdit.setGeometry(QtCore.QRect(250, 130, 150, 20))
        self.phone_lineEdit.setObjectName("phone_lineEdit")

        self.birth_lineEdit = QtWidgets.QDateEdit(Dialog)
        self.birth_lineEdit.setGeometry(QtCore.QRect(250, 180, 150, 20))
        self.birth_lineEdit.setObjectName("birth_lineEdit")

        self.add_btn = QtWidgets.QPushButton(Dialog)
        self.add_btn.setGeometry(QtCore.QRect(250, 220, 100, 20))
        self.add_btn.setObjectName("add_btn")

        self.add_btn.clicked.connect(lambda: self.addClicked(usernick))
        
        self.lable = QtWidgets.QLabel(Dialog)
        self.lable.setGeometry(QtCore.QRect(190, 10, 200, 50))

        font = QtGui.QFont()
        font.setPointSize(18)

        self.lable.setFont(font)
        self.lable.setObjectName("lable")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("sign up dialog")
        self.name_lable.setText("NAME")
        self.phone_lable.setText("PHONE")
        self.birth_lable.setText("BIRTH")
        self.add_btn.setText("Add Contact")
        self.lable.setText("Add Contact Form")

    def addClicked(self, usernick):
        name = self.name_lineEdit.text()
        phone = self.phone_lineEdit.text()
        birth = self.birth_lineEdit.text()
        if usernick != None:
            connection = mariadb.connection(host='localhost',user='contact', password='12345', database="contact_book_db")
            cur = connection.cursor()
            cur.execute("SELECT * FROM "+ usernick + " WHERE NAME = '" + name + "' AND PHONE = '" + phone + "' AND BIRTH = '" + birth + "'")
            result = cur.fetchone()
            if result == None:
                cur.execute("INSERT INTO " + usernick + " VALUES (?, ?, ?)", (name, phone, birth))
                connection.commit()
                connection.close()
                self.showMessageBox("Contact Added", "Contact added, you can close Add Contact Form.")
            else:
                self.showMessageBox("Contact didn't added", "This contact already exists.")

        self.qmainwindow = QMainWindow()
        self.mainwindow = Ui_main_window()
        self.mainwindow.setupUi(self.qmainwindow, usernick)
        self.qmainwindow.show()

    def showMessageBox(self, title, message):
        self.msgBox = QtWidgets.QMessageBox()
        self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
        self.msgBox.setWindowTitle(title)
        self.msgBox.setText(message)
        self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msgBox.exec_() 
        
class EditNameDialog(object):
    def setupEdittUi(self, Dialog, usernick, currentCol, const1, const2):
        Dialog.setObjectName("Edit Contact")
        Dialog.resize(300, 200)
        
        font = QtGui.QFont()
        font.setPointSize(10)

        self.value_lable = QtWidgets.QLabel(Dialog)
        self.value_lable.setGeometry(QtCore.QRect(25, 80, 70, 20))
        self.value_lable.setFont(font)
        self.value_lable.setAlignment(QtCore.Qt.AlignCenter)
        self.value_lable.setObjectName("value_lable")

        if currentCol == 2:
            self.dat_lineEdit = QtWidgets.QDateEdit(Dialog)
            self.dat_lineEdit.setGeometry(QtCore.QRect(100, 80, 150, 20))
            self.dat_lineEdit.setObjectName("dat_lineEdit")
        else:
            self.value_lineEdit = QtWidgets.QLineEdit(Dialog)
            self.value_lineEdit.setGeometry(QtCore.QRect(100, 80,  150, 20))
            self.value_lineEdit.setObjectName("value_lineEdit")

        self.edit_cont_btn = QtWidgets.QPushButton(Dialog)
        self.edit_cont_btn.setGeometry(QtCore.QRect(75, 120, 50, 20))
        self.edit_cont_btn.setObjectName("edit_cont_btn")

        self.edit_cont_btn.clicked.connect(lambda: self.editContClicked(usernick, currentCol, const1, const2))
        
        self.lable = QtWidgets.QLabel(Dialog)
        self.lable.setGeometry(QtCore.QRect(190, 10, 200, 50))

        font = QtGui.QFont()
        font.setPointSize(18)

        self.lable.setFont(font)
        self.lable.setObjectName("lable")

        self.retranslateUi(Dialog, currentCol)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog, currentCol):
        Dialog.setWindowTitle("Edit Contact dialog")
        if currentCol == 0:
            self.value_lable.setText("New Name")
        elif currentCol == 1:
            self.value_lable.setText("New Phone")
        elif currentCol == 2:
            self.value_lable.setText("New Date")
        self.edit_cont_btn.setText("Edit")

    def editContClicked(self, usernick, currentCol, const1, const2):
        if currentCol == 0: 
            connection = mariadb.connection(host='localhost',user='contact', password='12345', database="contact_book_db")
            cur = connection.cursor()
            cur.execute("UPDATE " + usernick + " SET NAME = '" + self.value_lineEdit.text() + "' WHERE PHONE = '" + str(const1) + "' AND BIRTH = '" + str(const2) + "'")
            connection.commit()
            connection.close()
        elif currentCol == 1: 
            connection = mariadb.connection(host='localhost',user='contact', password='12345', database="contact_book_db")
            cur = connection.cursor()
            cur.execute("UPDATE " + usernick + " SET PHONE = '" + self.value_lineEdit.text() + "' WHERE NAME = '" + str(const1) + "' AND BIRTH = '" + str(const2) + "'")
            connection.commit()
            connection.close()
        elif currentCol == 2: 
            connection = mariadb.connection(host='localhost',user='contact', password='12345', database="contact_book_db")
            cur = connection.cursor()
            cur.execute("UPDATE " + usernick + " SET BIRTH = '" + self.dat_lineEdit.text() + "' WHERE NAME = '" + str(const1) + "' AND PHONE = '" + str(const2) + "'")
            connection.commit()
            connection.close()
        else:
            self.showMessageBox("Error", "Please, select cell you want update")
        self.qmainwindow = QMainWindow()
        self.mainwindow = Ui_main_window()
        self.mainwindow.setupUi(self.qmainwindow, usernick)
        self.qmainwindow.show()

    def showMessageBox(self, title, message):
        self.msgBox = QtWidgets.QMessageBox()
        self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
        self.msgBox.setWindowTitle(title)
        self.msgBox.setText(message)
        self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msgBox.exec_()
        
class Ui_main_window(object):
    def setupUi(self, MainWindow, usernickname):
        MainWindow.setObjectName("main app")
        MainWindow.resize(800, 300)
        
        self.mdi = QtWidgets.QMdiArea()

        ########## right widget ##########
        self.rigthwidget = QtWidgets.QMdiSubWindow()
        self.mdi.addSubWindow(self.rigthwidget)
    
        font = QtGui.QFont()
        font.setPointSize(10)

        self.lable = QtWidgets.QLabel(self.rigthwidget)
        self.lable.setGeometry(10, 10, 300, 50)
        self.lable.setFont(font)
        self.lable.setObjectName("lable")

        self.lable1 = QtWidgets.QLabel(self.rigthwidget)
        self.lable1.setGeometry(10, 30, 300, 50)
        self.lable1.setFont(font)
        self.lable1.setObjectName("lable1")

        connection = mariadb.connection(host='localhost',user='contact', password='12345', database="contact_book_db")
        cur = connection.cursor()
        cur.execute("SELECT NAME, PHONE, BIRTH FROM " + usernickname + " GROUP BY NAME")
        data = cur.fetchall()
        connection.commit()
        connection.close()

        currentMonth = str(datetime.now().month)
        closebirth = []
        for d in data:
            if currentMonth == '10' and d[2][3] == '1':
                if d[2][4] == '0' or d[2][4] == '1':
                    closebirth.append(d)
            elif currentMonth == '11' and d[2][3] == '1':
                if d[2][4] == '1' or d[2][4] == '2':
                    closebirth.append(d)
            elif currentMonth == '12':
                if d[2][3] == '1' and d[2][4] == '2':
                    closebirth.append(d)
                elif d[2][3] == '0' and d[2][4] == '1':
                    closebirth.append(d)
            elif d[2][4] == currentMonth or d[2][4] == str(int(currentMonth)+1):
                if d[2][3] == '0':
                    closebirth.append(d)

        self.birthtable = QtWidgets.QTableWidget(self.rigthwidget)
        self.birthtable.setGeometry(100, 80,  215, 200)
        self.birthtable.setColumnCount(2)
        self.birthtable.setHorizontalHeaderLabels(["Name", "Birth"])
        for b in closebirth:
            rows = self.birthtable.rowCount()
            self.birthtable.setRowCount(rows + 1)
            self.birthtable.setItem(rows, 0, QtWidgets.QTableWidgetItem(b[0]))
            self.birthtable.setItem(rows, 1, QtWidgets.QTableWidgetItem(str(b[2])))
        

        ####### left widget ##########
        self.tabwid = QtWidgets.QTabWidget()

        ### tab 2 ###
        self.addContBtn = QPushButton(self.tabwid)
        self.addContBtn.setText("Add")
        self.addContBtn.setGeometry(340, 50, 100, 30)
        self.addContBtn.setObjectName("addContBtn")
        self.addContBtn.clicked.connect(lambda: self.addEntry(usernickname))
        
        self.delBtn = QPushButton(self.tabwid)
        self.delBtn.setText("Delete")
        self.delBtn.setGeometry(340, 100, 100,30)
        self.delBtn.clicked.connect(lambda: self.deleteRow(usernickname))
        
        self.editBtn = QPushButton(self.tabwid)
        self.editBtn.setText("Edit")
        self.editBtn.setGeometry(340, 150, 100,30)
        self.editBtn.clicked.connect(lambda: self.editCell(usernickname))

        self.table_view = QtWidgets.QTableWidget()
        self.table_view.setColumnCount(3)
        self.table_view.setHorizontalHeaderLabels(["Name", "Phone", "Birth"])   

        self.tabwid.addTab(self.table_view, "Contact Book")

        
        connection = mariadb.connection(host='localhost',user='contact', password='12345', database="contact_book_db")
        cur = connection.cursor()
        cur.execute("SELECT NAME, PHONE, BIRTH FROM " + usernickname + " GROUP BY NAME")
        data = cur.fetchall()
        for d in data:
            rows = self.table_view.rowCount()
            self.table_view.setRowCount(rows + 1)
            self.table_view.setItem(rows, 0, QtWidgets.QTableWidgetItem(d[0]))
            self.table_view.setItem(rows, 1, QtWidgets.QTableWidgetItem(str(d[1])))
            self.table_view.setItem(rows, 2, QtWidgets.QTableWidgetItem(str(d[2])))
        connection.commit()
        connection.close()

        groupABC=[]
        groupDEF=[]
        groupGHI=[]
        groupJKL=[]
        groupMNO=[]
        groupPQR=[]
        groupSTU=[]
        groupVW=[]
        groupXYZ=[]

        for d in data:
            if d[0][0] == 'a' or d[0][0] == 'b' or d[0][0] == 'c' or d[0][0] == 'A' or d[0][0] == 'B' or d[0][0] == 'C':
                groupABC.append(d)
            elif d[0][0] == 'd' or d[0][0] == 'e' or d[0][0] == 'f' or d[0][0] == 'D' or d[0][0] == 'E' or d[0][0] == 'F':
                groupDEF.append(d)
            elif d[0][0] == 'g' or d[0][0] == 'h' or d[0][0] == 'i' or d[0][0] == 'G' or d[0][0] == 'H' or d[0][0] == 'I':
                groupGHI.append(d)
            elif d[0][0] == 'j' or d[0][0] == 'k' or d[0][0] == 'l' or d[0][0] == 'J' or d[0][0] == 'K' or d[0][0] == 'L':
                groupJKL.append(d)
            elif d[0][0] == 'm' or d[0][0] == 'n' or d[0][0] == 'o' or d[0][0] == 'M' or d[0][0] == 'N' or d[0][0] == 'O':
                groupMNO.append(d)
            elif d[0][0] == 'p' or d[0][0] == 'q' or d[0][0] == 'r' or d[0][0] == 'P' or d[0][0] == 'Q' or d[0][0] == 'R':
                groupPQR.append(d)
            elif d[0][0] == 's' or d[0][0] == 't' or d[0][0] == 'u' or d[0][0] == 'S' or d[0][0] == 'T' or d[0][0] == 'U':
                groupSTU.append(d)
            elif d[0][0] == 'v' or d[0][0] == 'w'or d[0][0] == 'V' or d[0][0] == 'W':
                groupVW.append(d)
            elif d[0][0] == 'x' or d[0][0] == 'y' or d[0][0] == 'z' or d[0][0] == 'X' or d[0][0] == 'Y' or d[0][0] == 'Z':
                groupXYZ.append(d)

        ### tab ABC ###

        self.tabABC = QtWidgets.QTableWidget()
        self.tabABC.setColumnCount(3)
        self.tabABC.setHorizontalHeaderLabels(["Name", "Phone", "Birth"])

        self.tabwid.addTab(self.tabABC, "ABC")

        for line in groupABC:
            rows = self.tabABC.rowCount()
            self.tabABC.setRowCount(rows + 1)
            self.tabABC.setItem(rows, 0, QtWidgets.QTableWidgetItem(line[0]))
            self.tabABC.setItem(rows, 1, QtWidgets.QTableWidgetItem(str(line[1])))
            self.tabABC.setItem(rows, 2, QtWidgets.QTableWidgetItem(str(line[2])))


        ### tab DEF ###

        self.tabDEF = QtWidgets.QTableWidget()
        self.tabDEF.setColumnCount(3)
        self.tabDEF.setHorizontalHeaderLabels(["Name", "Phone", "Birth"])

        self.tabwid.addTab(self.tabDEF, "DEF")

        for line in groupDEF:
            rows = self.tabDEF.rowCount()
            self.tabDEF.setRowCount(rows + 1)
            self.tabDEF.setItem(rows, 0, QtWidgets.QTableWidgetItem(line[0]))
            self.tabDEF.setItem(rows, 1, QtWidgets.QTableWidgetItem(str(line[1])))
            self.tabDEF.setItem(rows, 2, QtWidgets.QTableWidgetItem(str(line[2])))

        ### tab GHI ###

        self.tabGHI = QtWidgets.QTableWidget()
        self.tabGHI.setColumnCount(3)
        self.tabGHI.setHorizontalHeaderLabels(["Name", "Phone", "Birth"])

        self.tabwid.addTab(self.tabGHI, "GHI")

        for line in groupGHI:
            rows = self.tabGHI.rowCount()
            self.tabGHI.setRowCount(rows + 1)
            self.tabGHI.setItem(rows, 0, QtWidgets.QTableWidgetItem(line[0]))
            self.tabGHI.setItem(rows, 1, QtWidgets.QTableWidgetItem(str(line[1])))
            self.tabGHI.setItem(rows, 2, QtWidgets.QTableWidgetItem(str(line[2])))
        
        ### tab JKL ###
        
        self.tabJKL = QtWidgets.QTableWidget()
        self.tabJKL.setColumnCount(3)
        self.tabJKL.setHorizontalHeaderLabels(["Name", "Phone", "Birth"])

        self.tabwid.addTab(self.tabJKL, "JKL")

        for line in groupJKL:
            rows = self.tabJKL.rowCount()
            self.tabJKL.setRowCount(rows + 1)
            self.tabJKL.setItem(rows, 0, QtWidgets.QTableWidgetItem(line[0]))
            self.tabJKL.setItem(rows, 1, QtWidgets.QTableWidgetItem(str(line[1])))
            self.tabJKL.setItem(rows, 2, QtWidgets.QTableWidgetItem(str(line[2])))
        
        ### tab MNO ###

        self.tabMNO = QtWidgets.QTableWidget()
        self.tabMNO.setColumnCount(3)
        self.tabMNO.setHorizontalHeaderLabels(["Name", "Phone", "Birth"])

        self.tabwid.addTab(self.tabMNO, "MNO")

        for line in groupMNO:
            rows = self.tabMNO.rowCount()
            self.tabMNO.setRowCount(rows + 1)
            self.tabMNO.setItem(rows, 0, QtWidgets.QTableWidgetItem(line[0]))
            self.tabMNO.setItem(rows, 1, QtWidgets.QTableWidgetItem(str(line[1])))
            self.tabMNO.setItem(rows, 2, QtWidgets.QTableWidgetItem(str(line[2])))
        
        ### tab PQR ###

        self.tabPQR = QtWidgets.QTableWidget()
        self.tabPQR.setColumnCount(3)
        self.tabPQR.setHorizontalHeaderLabels(["Name", "Phone", "Birth"])

        self.tabwid.addTab(self.tabPQR, "PQR")

        for line in groupPQR:
            rows = self.tabPQR.rowCount()
            self.tabPQR.setRowCount(rows + 1)
            self.tabPQR.setItem(rows, 0, QtWidgets.QTableWidgetItem(line[0]))
            self.tabPQR.setItem(rows, 1, QtWidgets.QTableWidgetItem(str(line[1])))
            self.tabPQR.setItem(rows, 2, QtWidgets.QTableWidgetItem(str(line[2])))
        
        ### tab STU ###

        self.tabSTU = QtWidgets.QTableWidget()
        self.tabSTU.setColumnCount(3)
        self.tabSTU.setHorizontalHeaderLabels(["Name", "Phone", "Birth"])

        self.tabwid.addTab(self.tabSTU, "STU")

        for line in groupSTU:
            rows = self.tabSTU.rowCount()
            self.tabSTU.setRowCount(rows + 1)
            self.tabSTU.setItem(rows, 0, QtWidgets.QTableWidgetItem(line[0]))
            self.tabSTU.setItem(rows, 1, QtWidgets.QTableWidgetItem(str(line[1])))
            self.tabSTU.setItem(rows, 2, QtWidgets.QTableWidgetItem(str(line[2])))
        
        ### tab VW ###

        self.tabVW = QtWidgets.QTableWidget()
        self.tabVW.setColumnCount(3)
        self.tabVW.setHorizontalHeaderLabels(["Name", "Phone", "Birth"])

        self.tabwid.addTab(self.tabVW, "VW")

        for line in groupVW:
            rows = self.tabVW.rowCount()
            self.tabVW.setRowCount(rows + 1)
            self.tabVW.setItem(rows, 0, QtWidgets.QTableWidgetItem(line[0]))
            self.tabVW.setItem(rows, 1, QtWidgets.QTableWidgetItem(str(line[1])))
            self.tabVW.setItem(rows, 2, QtWidgets.QTableWidgetItem(str(line[2])))
        
        ### tab XYZ ###

        self.tabXYZ = QtWidgets.QTableWidget()
        self.tabXYZ.setColumnCount(3)
        self.tabXYZ.setHorizontalHeaderLabels(["Name", "Phone", "Birth"])

        self.tabwid.addTab(self.tabXYZ, "XYZ")

        for line in groupXYZ:
            rows = self.tabXYZ.rowCount()
            self.tabXYZ.setRowCount(rows + 1)
            self.tabXYZ.setItem(rows, 0, QtWidgets.QTableWidgetItem(line[0]))
            self.tabXYZ.setItem(rows, 1, QtWidgets.QTableWidgetItem(str(line[1])))
            self.tabXYZ.setItem(rows, 2, QtWidgets.QTableWidgetItem(str(line[2])))
        
        ###  ###
        self._contactwidget = QtWidgets.QMdiSubWindow() 
        self._contactwidget.setMinimumWidth(450) 
        self._contactwidget.setWidget(self.tabwid)
        
        self.mdi.addSubWindow(self._contactwidget)
        
        self.mdi.tileSubWindows()
        MainWindow.setCentralWidget(self.mdi)

        self.retranslateUi(MainWindow, usernickname)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.table_view.resizeColumnsToContents()

    def retranslateUi(self, MainWindow, usernickname):
        MainWindow.setWindowTitle("MainWindow")
        self.lable.setText('Welcome to main app ' + usernickname + '!')
        self.lable1.setText("Nearest Birthdays")

    def addEntry(self, usernickname):
        self.addcontwindow = QDialog()
        self.contui = addContactToBookDialog()
        self.contui.setupContactUi(self.addcontwindow, usernickname)
        self.addcontwindow.show()

    def deleteRow(self, usernickname):
        row = self.table_view.selectedItems()
        if len(row) == 3:
            for r in row:
                connection = mariadb.connection(host='localhost',user='contact', password='12345', database="contact_book_db")
                cur = connection.cursor()
                cur.execute("DELETE FROM " + usernickname + " WHERE NAME = '" + str(row[0].text()) + "' AND PHONE = '" + str(row[1].text()) + "' AND BIRTH = '" + str(row[2].text()) + "'")
                connection.commit()
                connection.close()
                self.qmainwindow = QMainWindow()
                self.mainwindow = Ui_main_window()
                self.mainwindow.setupUi(self.qmainwindow, usernickname)
                self.qmainwindow.show()
        else:
            self.showMessageBox("Warning", "Please, select full row.")

    def editCell(self, usernickname):
        r = self.table_view.currentRow()
        c = self.table_view.currentColumn()
        if c == 0: 
            self.editcontwindow = QDialog()
            self.editui = EditNameDialog()
            self.editui.setupEdittUi(self.editcontwindow, usernickname, c, self.table_view.item(r, 1).text(), self.table_view.item(r, 2).text())
            self.editcontwindow.show()
        elif c == 1: 
            self.editcontwindow = QDialog()
            self.editui = EditNameDialog()
            self.editui.setupEdittUi(self.editcontwindow, usernickname, c, self.table_view.item(r, 0).text(), self.table_view.item(r, 2).text())
            self.editcontwindow.show()
        elif c == 2: 
            self.editcontwindow = QDialog()
            self.editui = EditNameDialog()
            self.editui.setupEdittUi(self.editcontwindow, usernickname, c, self.table_view.item(r, 0).text(), self.table_view.item(r, 1).text())
            self.editcontwindow.show()
        
        self.qmainwindow = QMainWindow()
        self.mainwindow = Ui_main_window()
        self.mainwindow.setupUi(self.qmainwindow, usernickname)
        self.qmainwindow.show()
    
    def showMessageBox(self, title, message):
        self.msgBox = QtWidgets.QMessageBox()
        self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
        self.msgBox.setWindowTitle(title)
        self.msgBox.setText(message)
        self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msgBox.exec_()

        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_dialog_Login()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())