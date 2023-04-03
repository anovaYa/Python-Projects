import sys
import pymongo
from PyQt5 import QtGui, QtCore, QtWidgets
from window import *


class Gui(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.centerOnScreen()
        self.authorization_status = False
        self.client = pymongo.MongoClient(
            "mongodb+srv://anova:12345@cluster0.ida1zgk.mongodb.net/?retryWrites=true&w=majority")
        self.ui.singin_button.clicked.connect(self.login)
        self.ui.singup_button.clicked.connect(self.singup)

    def show_message(self, title, message):
        msg = QtWidgets.QMessageBox(1, title, message)
        msg.setStyleSheet("color:white;background:rgb(14, 24, 33)")
        msg.exec()

    def check_data(self):
        login = self.ui.login_line.text()
        password = self.ui.pw_line.text()

        if login and password:
            search_login = self.client.testdata.testcoll.find_one({'name': login})
            if search_login:
                return "exists"
            else:
                return "not_found"
        else:
            return "no_data_available"

    def login(self):
        if self.authorization_status is False:
            result = self.check_data()

            if result == "exists":
                login = self.ui.login_line.text()
                password = self.ui.pw_line.text()
                document = self.client.testdata.testcoll.find_one({'name': login})

                if document and password == document['password']:
                    self.show_message('Notification', "Successful login")
                    self.authorization_status = True
                else:
                    self.show_message('Error', "Invalid data")

            elif result == "not_found":
                self.show_message('Notification', "No such user is registered")

            elif result == "no_data_available":
                self.show_message('Error', "Enter the data ")

        else:
            message = "A user with this login address already exists"
            self.show_message('Error', message)

    def singup(self):
        if self.authorization_status is False:
            result = self.check_data()

            if result == "exists":
                message = "A user with this login address already exists"
                self.show_message('Error', message)

            elif result == "not_found":
                data = {
                    'name': self.ui.login_line.text(),
                    'password': self.ui.pw_line.text()
                }
                self.client.testdata.testcoll.insert_one(data)
                message = "You have successfully registered"
                self.show_message('Notification', message)
                self.authorization_status = True
            else:
                self.show_message('Error', 'You already have an account')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mywindow = Gui()
    mywindow.show()
    sys.exit(app.exec_())
