# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWidget.ui'
#
# Created: Tue May 14 11:48:13 2013
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        MainWidget.setObjectName(_fromUtf8("MainWidget"))
        MainWidget.resize(1000, 600)
        MainWidget.setWindowTitle(QtGui.QApplication.translate("MainWidget", "PySchedGUI", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayoutWidget = QtGui.QWidget(MainWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 261, 81))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.AddJobBtn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.AddJobBtn.setText(QtGui.QApplication.translate("MainWidget", "New Job", None, QtGui.QApplication.UnicodeUTF8))
        self.AddJobBtn.setObjectName(_fromUtf8("AddJobBtn"))
        self.verticalLayout.addWidget(self.AddJobBtn)
        self.RefreshBtn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.RefreshBtn.setText(QtGui.QApplication.translate("MainWidget", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.RefreshBtn.setObjectName(_fromUtf8("RefreshBtn"))
        self.verticalLayout.addWidget(self.RefreshBtn)
        self.JobTable = QtGui.QTableView(MainWidget)
        self.JobTable.setGeometry(QtCore.QRect(270, 0, 721, 421))
        self.JobTable.setAlternatingRowColors(True)
        self.JobTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.JobTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.JobTable.setObjectName(_fromUtf8("JobTable"))
        self.WSTable = QtGui.QTableView(MainWidget)
        self.WSTable.setGeometry(QtCore.QRect(0, 430, 991, 161))
        self.WSTable.setObjectName(_fromUtf8("WSTable"))

        self.retranslateUi(MainWidget)
        QtCore.QMetaObject.connectSlotsByName(MainWidget)

    def retranslateUi(self, MainWidget):
        pass

