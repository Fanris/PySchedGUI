# -*- coding: utf-8 -*-
'''
Created on 2013-05-27 13:13
@summary: Application Window
@author: predki
'''
from PySide import QtGui, QtCore

from Widgets.MainWidget import MainWidget
from Dialogs.LoginDialog import LoginDialog
from Dialogs.AdminDialog import AdminDialog

import Icons

class GUI(QtGui.QMainWindow):
    def __init__(self, pySchedUI):
        QtGui.QMainWindow.__init__(self)

        self.pySchedUI = pySchedUI
        self.adminMode = False

        self.resize(1000, 600)
        self.setWindowTitle('PySched GUI v{} (PySide)'.format(self.pySchedUI.version))


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

        connectionTb = self.addToolBar("Connection Toolbar" )
        self.connectAct = connectionTb.addAction(QtGui.QIcon(":/images/connect.png"), 'Connect to Server')
        QtCore.QObject.connect(self.connectAct, QtCore.SIGNAL("triggered()"), self.connectBtn)

        self.disconnectAct = connectionTb.addAction(QtGui.QIcon(":/images/disconnect.png"), 'Disconnect from Server')
        QtCore.QObject.connect(self.disconnectAct, QtCore.SIGNAL("triggered()"), self.closeConnection)

        jobTb = self.addToolBar("Job Toolbar")
        act = jobTb.addAction(QtGui.QIcon(":/images/newJob.png"), 'New Job')
        QtCore.QObject.connect(act, QtCore.SIGNAL("triggered()"), self.newJob)

        act = jobTb.addAction(QtGui.QIcon(":/images/openJob.png"), 'Open Job')
        QtCore.QObject.connect(act, QtCore.SIGNAL("triggered()"), self.openJob)

        self.adminToolBar = None

        if not self.pySchedUI.userId or not self.pySchedUI.rsaKey:
            if self.showLoginDialog():
                self.openConnection()
            else:
                self.statusBar().showMessage("Connection failed!")
                self.mainWidget.setDisabled(True)
                self.disconnectAct.setEnabled(False)
                self.exit()
        else:
            self.openConnection()

        self.timer = QtCore.QTimer(parent=self)
        self.timer.setInterval(10000)
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.mainWidget.updateTables)
        self.timer.start()

    def openConnection(self):
        if self.pySchedUI.openConnection():
            self.statusBar().showMessage('Connected')
            self.isConnected = True
            self.connectAct.setEnabled(False)
            self.disconnectAct.setEnabled(True)
            self.mainWidget.setEnabled(True)
            if self.pySchedUI.isAdmin:
                self.showAdminToolBar()
                
            self.mainWidget.updateTables()
        else:
            self.statusBar().showMessage("Connection failed!")
            self.isConnected = False
            self.connectAct.setEnabled(True)
            self.disconnectAct.setEnabled(False)
            if self.adminToolBar:
                self.adminToolBar.setEnabled(False)

    def closeConnection(self):
        self.pySchedUI.closeConnection()   
        self.isConnected = False
        self.connectAct.setEnabled(True)
        self.disconnectAct.setEnabled(False)      
        self.mainWidget.setEnabled(False)
        self.statusBar().showMessage("Disconnected by User")
        if self.adminToolBar:
            self.removeToolbar(self.adminToolBar)

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

    def showGUI(self):
        self.center()
        self.show()

    def showAdminToolBar(self):
        spacer = QtGui.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding) 

        self.adminModeCheckBox = QtGui.QCheckBox("Admin Mode")
        QtCore.QObject.connect(self.adminModeCheckBox, QtCore.SIGNAL("stateChanged(int)"), self.changeAdminMode)
       
        self.adminToolBar = QtGui.QToolBar("Admin Toolbar")        
        self.addToolBar(self.adminToolBar)
        self.adminToolBar.addWidget(spacer)

        self.adminToolBar.addWidget(self.adminModeCheckBox)
        act = self.adminToolBar.addAction(QtGui.QIcon(":images/adminMode.png"), "Admin Menu")
        QtCore.QObject.connect(act, QtCore.SIGNAL("triggered()"), self.showAdminMenu)

    def connectBtn(self):
        self.showLoginDialog()
        self.openConnection()

    def showAdminMenu(self):
        adminDialog = AdminDialog(self.pySchedUI, parent=self)
        if adminDialog.exec_():
            pass

    def showLoginDialog(self):
        rsa = self.pySchedUI.loadRSA()
        login = LoginDialog(self, rsa)
        if login.exec_():
            try:
                user, rsa, save = login.getInfos()
                self.pySchedUI.userId = user
                self.pySchedUI.rsaKey = rsa
                if save:
                    self.pySchedUI.saveRSA(rsa)
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

    def changeAdminMode(self):
        if self.adminModeCheckBox:
            self.adminMode = self.adminModeCheckBox.isChecked()

        self.mainWidget.updateTables()

    def exit(self):
        self.pySchedUI.closeConnection()
        self.close()

    def forceScheduling(self):
        self.pySchedUI.forceSchedule()
