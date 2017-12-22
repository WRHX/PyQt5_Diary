# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_diaryDisplay.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(700, 700)
        self.textBrowser_displayPosts = QtWidgets.QTextBrowser(dialog)
        self.textBrowser_displayPosts.setEnabled(True)
        self.textBrowser_displayPosts.setGeometry(QtCore.QRect(0, 0, 700, 700))
        self.textBrowser_displayPosts.setObjectName("textBrowser_displayPosts")

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "Diary entries"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Ui_dialog()
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())

