# -*- coding: utf-8 -*-
'''
Created on 2013-05-27 13:13
@summary: Application Window
@author: predki
'''
from PyQt4 import QtGui, QtCore

from MainWidget import MainWidget
from LoginDialog import LoginDialog

import Icons

class GUI(QtGui.QMainWindow):
    def __init__(self, pySchedUI):
        QtGui.QMainWindow.__init__(self)

        self.pySchedUI = pySchedUI
        self.adminMode = False

        self.resize(1000, 600)
        self.setWindowTitle('PySched GUI v2.0')

        self.mainWidget = MainWidget(parent=self)
        self.setCentralWidget(self.mainWidget)
        self.isConnected = False

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        act = fileMenu.addAction("New Job")
        QtCore.QObject.connect(act, QtCore.SIGNAL("triggered()"), self.newJob)
        act = fileMenu.addAction("New Job from Template")
        QtCore.QObject.connect(act, QtCore.SIGNAL("triggered()"), self.openJob)
        fileMenu.addSeparator()
        act = fileMenu.addAction("Exit")        
        QtCore.QObject.connect(act, QtCore.SIGNAL("triggered()"), self.exit)

        toolbar = self.addToolBar("New Job")
        act = toolbar.addAction(QtGui.QIcon(":/images/newJob.png"), 'New Job')
        QtCore.QObject.connect(act, QtCore.SIGNAL("triggered()"), self.newJob)

        act = toolbar.addAction(QtGui.QIcon(":/images/openJob.png"), 'Open Job')
        QtCore.QObject.connect(act, QtCore.SIGNAL("triggered()"), self.openJob)

        if not self.pySchedUI.userId or not self.pySchedUI.rsaKey:
            if self.showLoginDialog():
                self.openConnection()
            else:
                self.exit()
        else:
            self.openConnection()

        if self.isConnected:
            self.mainWidget.updateTables()

    def openConnection(self):
        if self.pySchedUI.openConnection():
            self.statusBar().showMessage('Connected')
            self.isConnected = True
        else:
            self.statusBar().showMessage("Connection failed!")

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

    def showGUI(self):
        self.center()
        self.show()

    def showLoginDialog(self):
        login = LoginDialog(self)
        if login.exec_():
            try:
                user, rsa = login.getInfos()
                self.pySchedUI.userId = user
                self.pySchedUI.rsaKey = rsa
                return True
            except:
                self.pySchedUI.logger.info("Fehler!!!")
        return False    

    def newJob(self):
        self.mainWidget.showAddJobDialog()

    def openJob(self):        
        templatePath = QtGui.QFileDialog.getOpenFileName(self, "Select a Template file")
        if templatePath:
            self.mainWidget.showAddJobDialog(templatePath=templatePath)

    def exit(self):
        self.pySchedUI.closeConnection()
        self.close()
