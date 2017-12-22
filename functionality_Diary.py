'''
App description:
User can post text to a database corresponding to a specific date, and retreive
posts from a specific date to read them.

TODO:
    -   Make program windows independentish of display monitor or at least resize it well.
        (This should be fixed in Qt designer, when creating the GUI)
'''

import sys
import time
from Ui_Diary import Ui_MainWindow
from Ui_diaryDisplay import Ui_dialog
from PyQt5 import QtCore, QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlError
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QMessageBox, QDialog

class Dialog(Ui_dialog):
    '''
    Make a class for the dialog window to be used to display the posts of selected date.
    This class is called in the showDialog method of the MainWindow class.
    '''
    def __init__(self,dialog):
        Ui_dialog.__init__(self)
        self.setupUi(dialog)

class MainWindow(Ui_MainWindow):
    '''
    Define the Mainwindow and its methods. Stuff in the __init__ method is run
    upon creation of an object of this class. (In our case once
    (from if __name__ == '__main__') when functionality_Diary.py is run)
    '''
    def __init__(self,window):
        Ui_MainWindow.__init__(self)
        self.setupUi(window)

        self.db = None #Initialize db variable so we can work with it globally
        self.dialog = None # will become a popup window (poor explanation yes)
        self.progdialog = None # will become the popup window object

        self.establishDatabaseConnection()

        self.createTable() #Creates a table if it does not exists in the database yet.
        self.postButton.clicked.connect(self.postToDiary) #Query to enter a string into db.
        self.openButton.clicked.connect(self.readFromDiary)

        app.aboutToQuit.connect(self.closeDataseConnection)

    def establishDatabaseConnection(self):
        '''
        This method creates a default database connection.
        See http://pyqt.sourceforge.net/Docs/PyQt4/qsqldatabase.html for more information.
        If the actual database file did not exist yet it gets created when setDatabaseName is called.
        '''
        self.db = QSqlDatabase.addDatabase('QSQLITE') #If a second str arg was given it would be the name of the connection.
        self.db.setDatabaseName('diarydb.db') #If file doesn't exist it's created here.
        ok = self.db.open() #Open the connection to datbase so we can query it.
        #print(str(ok)) #When this says true the connection to the database is succesful.

    def createTable(self):
        '''
        This method calls creates the table we will use in the database if it does not
        exist already. Commented is an example of how to test if a (general SQLite) query was succesful.
        '''
        query = QSqlQuery()
        x = query.exec_("CREATE TABLE IF NOT EXISTS posts (concatDate int, post varchar(10))")
        # x = TRUE if succes, false if failed.
        #print(str(x))
        #y = query.lastError() #An error object is pointed at, don't know how to access adress and read contents.

    def postToDiary(self):
        ''''
        Collects all the data from the input widgets and sends it to database.
        '''
        concatDate, postContent = self.getContents()
        #Now the sending to the database part.
        query = QSqlQuery()
        query.prepare("INSERT INTO posts (concatDate, post) VALUES (:concatDate,:post)")
        query.bindValue(":concatDate", concatDate) #This is needed to get python variables into
        query.bindValue(":post", postContent)      #the SQLite query.
        x = query.exec_()
        self.textEdit.clear()

    def readFromDiary(self):
        '''
        Here we retreive all the entries in the database from a specified date, which is selected
        by the user in the calendarWidget. First we get the selected date. Then we send an SQLite query
        to get all the posts where the selected date matches the date in the database.
        See http://pyqt.sourceforge.net/Docs/PyQt4/qsqlquery.html on how to access data from a query.
        There the explanation of the while loop in the end of this function is given, but in
        different syntax (C or c++ or something).
        '''
        self.textEdit.clear()
        requested_concatDate, not_used = self.getContents() #not_used contains the contents of textEdit which don't use.
        day, month, year = self.parseConcatDate(requested_concatDate) #this is used in the for loop later in the method.

        query = QSqlQuery() # Create query object
        query.prepare("SELECT post FROM posts WHERE concatDate == (:requested_concatDate)")
        query.bindValue(":requested_concatDate", requested_concatDate) #This is needed to get python variables into SQLite query
        x = query.exec_()

        '''
        In the following a list is used to transfer query content to the dialog for printing.
        The list acts like a middle man and it's possible to take it out: Put self.showDialog above the
        while loop and append textBrowser_displayPosts in the while loop.
        '''
        contentList = []
        while query.next():
            content = query.value(0)#.toString()
            contentList.append(query.value(0))

        self.showDialog()
        for n in range(0,len(contentList)):
            self.progdialog.textBrowser_displayPosts.append('Entry '+ str(n+1) + ' on ' + day +' '+ self.getMonthName(int(month)) +' ' + year + ' is:')
            self.progdialog.textBrowser_displayPosts.append(contentList[n])
            self.progdialog.textBrowser_displayPosts.append('')

    def getContents(self):
        '''
        get the selected date from the calendarWidget and put it in the format used in the database.
        Also get the entered text from the textEdit input field.
        '''
        dateToPost = self.calendarWidget.selectedDate()
        concatDate = self.concatenateDate(dateToPost) #This is format stored in db.
        postContent = self.textEdit.toPlainText() #This is a string. Gets contents of textEdit.
        return (concatDate, postContent)

    def concatenateDate(self,dateToPost):
        '''
        Turn individual day, month, year integers into a concatenated string with chosen format
        d(d)_m(m)_yyyy.
        2 remarks:
            -   d(d)_m(m)_yyyy is a bad format (how to decide which integers belong to day/month)
            -   Probably a cleaner way by using different dateToPost method.
        '''
        dayStr = str(dateToPost.day())
        monthStr = str(dateToPost.month())
        yearStr = str(dateToPost.year())
        concatDate = dayStr+'_'+monthStr+'_'+yearStr #This is format stored in db.
        return concatDate

    def parseConcatDate(self, concatDate):
        '''
        Retreive the day, month, year numbers from the concatDate string.
        '''
        day, month, year = concatDate.split('_')
        return day,month,year

    def getMonthName(self,monthNumber):
        '''
        Returns the string month name corresponding to the month number.
        '''
        monthDictionary ={1:'January',
        2:'February',
        3:'March',
        4:'April',
        5:'May',
        6:'June',
        7:'Juli',
        8:'September',
        9:'August',
        10:'October',
        11:'November',
        12:'December'}
        return monthDictionary[monthNumber]

    def showDialog(self):
        '''
        Create a Dialog class object (pop up window to display posts from selected date).
        self.dialog is used to avoid Dialog being removed by garbage collector (it's like a global variable).
        The structure of this code is the same as the window/QMainWindow/MainWindow structure.
        '''
        self.dialog = QDialog()
        self.progdialog = Dialog(self.dialog) # this is the object that inherits the Ui_dialog stuff
        self.dialog.show()

    def closeDataseConnection(self):
        '''
        Closes the database (no more querying) and the removes the connection object.
        This method is run when program is closed in whatever way.
        '''
        self.db.close() # have to close the database before we can remove the dabase connection
        self.db.removeDatabase('testdb.db') # removes the database connection
        print('Database connection removed.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()

    prog = MainWindow(window)
    window.show()
    sys.exit(app.exec_())
