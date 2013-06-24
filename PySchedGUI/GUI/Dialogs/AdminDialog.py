# -*- coding: utf-8 -*-
'''
Created on 2013-06-04 12:25
@summary: 
@author: Martin Predki
'''

from PyQt4 import QtCore, QtGui

from PySchedGUI.GUI.Widgets.UserTable import UserTable
from PySchedGUI.GUI.Widgets.ProgramTable import ProgramTable

from UserDialog import UserDialog
from ProgramDialog import ProgramDialog

from PySchedGUI.PySchedUI.DataStructures import User, Program

class AdminDialog(QtGui.QDialog):
    def __init__(self, pySchedUI, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.pySchedUI = pySchedUI
        self.resize(720, 400)
        self.setWindowTitle("Admin Menu")
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(10, 360, 700, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)

        self.tabWidget = QtGui.QTabWidget(parent=self)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 700, 340))
        
        # ===== CONTROL WIDGET
        self.controlWidget = QtGui.QWidget()

        forceSchedulingBtn = QtGui.QPushButton("Force scheduling", parent=self.controlWidget)
        forceSchedulingBtn.setGeometry(QtCore.QRect(10, 10, 120, 24))
        QtCore.QObject.connect(forceSchedulingBtn, QtCore.SIGNAL("clicked()"), self.pySchedUI.forceSchedule)

        checkJobsBtn = QtGui.QPushButton("Force check jobs", parent=self.controlWidget)
        checkJobsBtn.setGeometry(QtCore.QRect(10, 44, 120, 24))
        QtCore.QObject.connect(forceSchedulingBtn, QtCore.SIGNAL("clicked()"), self.pySchedUI.checkJobs)

        shutdownServerBtn = QtGui.QPushButton("Shutdown Server", parent=self.controlWidget)
        shutdownServerBtn.setGeometry(QtCore.QRect(10, 78, 120, 24))
        QtCore.QObject.connect(shutdownServerBtn, QtCore.SIGNAL("clicked()"), self.shutdownServer)

        self.tabWidget.addTab(self.controlWidget, "General")

        # ===== Scheduling Parameter
        self.schedulingParams = self.pySchedUI.getSchedulingParams()
        self.schedulingParamsTab = QtGui.QWidget()
        self.schedulingParamWidget = QtGui.QWidget(self.schedulingParamsTab)
        self.schedulingParamWidget.setGeometry(QtCore.QRect(10, 10, 680, 270))

        self.updateBtn = QtGui.QPushButton("Update", parent=self.schedulingParamsTab)
        self.updateBtn.setGeometry(QtCore.QRect(570, 280, 120, 30))
        self.updateBtn.setEnabled(False)
        QtCore.QObject.connect(self.updateBtn, QtCore.SIGNAL("clicked()"), self.updateSchedulingParams)

        self.formLayout = QtGui.QFormLayout(self.schedulingParamWidget)
        self.formLayout.setRowWrapPolicy(QtGui.QFormLayout.WrapAllRows)
        self.formLayout.setContentsMargins(10, 10, 10, 10)

        label = QtGui.QLabel(self.schedulingParamWidget)
        label.setText("CPU load threshold:")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, label)
        
        self.cpuThresholdWidget = QtGui.QSpinBox(self.schedulingParamWidget)
        self.cpuThresholdWidget.setMinimum(0)
        self.cpuThresholdWidget.setMaximum(101)
        self.cpuThresholdWidget.setValue(self.schedulingParams.get("cpuThreshold", 20))               
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.cpuThresholdWidget)
        QtCore.QObject.connect(self.cpuThresholdWidget, QtCore.SIGNAL("valueChanged(int)"), self.enableUpdateBtn)      

        label = QtGui.QLabel(self.schedulingParamWidget)
        label.setText("Unused cpu penality:")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, label)
        
        self.unusedCpuPenalityWidget = QtGui.QSpinBox(self.schedulingParamWidget)
        self.unusedCpuPenalityWidget.setMinimum(0)
        self.unusedCpuPenalityWidget.setMaximum(10000)
        self.unusedCpuPenalityWidget.setValue(self.schedulingParams.get("unusedCpuPenality", 100))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.unusedCpuPenalityWidget)
        QtCore.QObject.connect(self.unusedCpuPenalityWidget, QtCore.SIGNAL("valueChanged(int)"), self.enableUpdateBtn)

        label = QtGui.QLabel(self.schedulingParamWidget)
        label.setText("Usable cpu bonus:")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, label)
        
        self.usableCpuBonusWidget = QtGui.QSpinBox(self.schedulingParamWidget)
        self.usableCpuBonusWidget.setMinimum(0)
        self.usableCpuBonusWidget.setMaximum(10000)
        self.usableCpuBonusWidget.setValue(self.schedulingParams.get("usableCpuBonus", 100))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.usableCpuBonusWidget)
        QtCore.QObject.connect(self.usableCpuBonusWidget, QtCore.SIGNAL("valueChanged(int)"), self.enableUpdateBtn)

        label = QtGui.QLabel(self.schedulingParamWidget)
        label.setText("Unused program penality:")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, label)
        
        self.unusedProgramPenalityWidget = QtGui.QSpinBox(self.schedulingParamWidget)
        self.unusedProgramPenalityWidget.setMinimum(0)
        self.unusedProgramPenalityWidget.setMaximum(10000)
        self.unusedProgramPenalityWidget.setValue(self.schedulingParams.get("unsedProgramPenality", 100))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.unusedProgramPenalityWidget)        
        QtCore.QObject.connect(self.unusedProgramPenalityWidget, QtCore.SIGNAL("valueChanged(int)"), self.enableUpdateBtn)

        label = QtGui.QLabel(self.schedulingParamWidget)
        label.setText("Active user penality:")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, label)
        
        self.activeUserPenalityWidget = QtGui.QSpinBox(self.schedulingParamWidget)
        self.activeUserPenalityWidget.setMinimum(0)
        self.activeUserPenalityWidget.setMaximum(10000)
        self.activeUserPenalityWidget.setValue(self.schedulingParams.get("activeUserPenality", 100))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.activeUserPenalityWidget)   
        QtCore.QObject.connect(self.activeUserPenalityWidget, QtCore.SIGNAL("valueChanged(int)"), self.enableUpdateBtn) 

        label = QtGui.QLabel(self.schedulingParamWidget)
        label.setText("Reserved cpus for users:")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, label)
        
        self.cpusForUsersWidget = QtGui.QSpinBox(self.schedulingParamWidget)
        self.cpusForUsersWidget.setMinimum(0)
        self.cpusForUsersWidget.setMaximum(10000)
        self.cpusForUsersWidget.setValue(self.schedulingParams.get("cpusForUsers", 1))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.cpusForUsersWidget)
        QtCore.QObject.connect(self.cpusForUsersWidget, QtCore.SIGNAL("valueChanged(int)"), self.enableUpdateBtn)

        self.tabWidget.addTab(self.schedulingParamsTab, "Scheduling Parameter")

        # ===== USER WIDGET
        self.userWidget = QtGui.QWidget()
        newUserBtn = QtGui.QPushButton("New User", parent=self.userWidget)
        newUserBtn.setGeometry(QtCore.QRect(10, 10, 100, 24))
        QtCore.QObject.connect(newUserBtn, QtCore.SIGNAL("clicked()"), self.showNewUserDialog)

        editUserBtn = QtGui.QPushButton("Edit User", parent=self.userWidget)
        editUserBtn.setGeometry(QtCore.QRect(10, 44, 100, 24))
        QtCore.QObject.connect(editUserBtn, QtCore.SIGNAL("clicked()"), self.showEditUserDialog)

        deleteUserBtn = QtGui.QPushButton("Delete User", parent=self.userWidget)
        deleteUserBtn.setGeometry(QtCore.QRect(10, 78, 100, 24))
        QtCore.QObject.connect(deleteUserBtn, QtCore.SIGNAL("clicked()"), self.deleteUser)        

        self.userTable = UserTable(self, self.userWidget)
        self.userTable.setGeometry(QtCore.QRect(120, 10, 570, 300))

        self.tabWidget.addTab(self.userWidget, "Users")

        # ===== PROGRAM WIDGET
        self.programWidget = QtGui.QWidget()
        newProgramBtn = QtGui.QPushButton("New Program", parent=self.programWidget)
        newProgramBtn.setGeometry(QtCore.QRect(10, 10, 100, 24))
        QtCore.QObject.connect(newProgramBtn, QtCore.SIGNAL("clicked()"), self.showNewProgramDialog)

        editProgramBtn = QtGui.QPushButton("Edit Program", parent=self.programWidget)
        editProgramBtn.setGeometry(QtCore.QRect(10, 44, 100, 24))
        QtCore.QObject.connect(editProgramBtn, QtCore.SIGNAL("clicked()"), self.showEditProgramDialog)

        deleteProgramBtn = QtGui.QPushButton("Delete Program", parent=self.programWidget)
        deleteProgramBtn.setGeometry(QtCore.QRect(10, 78, 100, 24))
        QtCore.QObject.connect(deleteProgramBtn, QtCore.SIGNAL("clicked()"), self.deleteProgram)     

        self.programTable = ProgramTable(self, self.programWidget)
        self.programTable.setGeometry(QtCore.QRect(120, 10, 570, 300))        

        self.tabWidget.addTab(self.programWidget, "Programs")

        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)    
        QtCore.QMetaObject.connectSlotsByName(self)    

        self.userTable.updateTable(self.pySchedUI.getUsers())
        self.programTable.updateTable(self.pySchedUI.getPrograms())


    def showNewUserDialog(self):
        userDialog = UserDialog(parent=self)
        if userDialog.exec_():
            user = userDialog.getInfos()
            self.pySchedUI.createUser(user)
            self.userTable.updateTable(self.pySchedUI.getUsers())

    def showEditUserDialog(self):
        row = None
        for idx in self.userTable.selectedIndexes():
            row = idx.row()

        u = User()
        u.id = int(self.userTable.item(row, 0).text())
        u.email = str(self.userTable.item(row, 1).text())
        u.firstName = str(self.userTable.item(row, 2).text())
        u.lastName = str(self.userTable.item(row, 3).text())
        u.admin = str(self.userTable.item(row, 4).text()) == "True"

        userDialog = UserDialog(parent=self, user=u)
        if userDialog.exec_():
            user = userDialog.getInfos()
            self.pySchedUI.createUser(user)
            self.userTable.updateTable(self.pySchedUI.getUsers())


    def deleteUser(self):
        row = None
        for idx in self.userTable.selectedIndexes():
            row = idx.row()

        email = str(self.userTable.item(row, 1).text())
        if QtGui.QMessageBox.question(self, 
            "Deleting User...", 
            "Are you sure you want to delete the user: {}".format(email),
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.No,
            QtGui.QMessageBox.No) == QtGui.QMessageBox.Ok:
            self.parent().pySchedUI.deleteUser(email)
            self.userTable.updateTable(self.pySchedUI.getUsers())       

    def showNewProgramDialog(self):
        programDialog = ProgramDialog(parent=self)
        if programDialog.exec_():
            program = programDialog.getInfos()
            self.pySchedUI.addProgram(program)
            self.programTable.updateTable(self.pySchedUI.getPrograms())

    def showEditProgramDialog(self):
        row = None
        for idx in self.programTable.selectedIndexes():
            row = idx.row()

        program = Program()
        program.id = int(self.programTable.item(row, 0).text())
        program.programName = str(self.programTable.item(row, 1).text())
        program.programPath = str(self.programTable.item(row, 2).text())
        program.programExec = str(self.programTable.item(row, 3).text())
        program.programVersion = str(self.programTable.item(row, 4).text())

        programDialog = ProgramDialog(parent=self, program=program)
        if programDialog.exec_():
            program = programDialog.getInfos()
            self.pySchedUI.addProgram(program)
            self.programTable.updateTable(self.pySchedUI.getPrograms())

    def deleteProgram(self):
        row = None
        for idx in self.programTable.selectedIndexes():
            row = idx.row()

        programName = str(self.programTable.item(row, 1).text())
        if QtGui.QMessageBox.question(self, 
            "Deleting User...", 
            "Are you sure you want to delete the program: {}".format(programName),
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.No,
            QtGui.QMessageBox.No) == QtGui.QMessageBox.Ok:
            self.pySchedUI.deleteProgram(programName)
            self.programTable.updateTable(self.pySchedUI.getPrograms())     

    def shutdownServer(self):
        if QtGui.QMessageBox.question(self, 
            "Shutdown Server...", 
            "Are you sure you want to shutdown the server?",
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.No,
            QtGui.QMessageBox.No) == QtGui.QMessageBox.Ok:
            self.pySchedUI.shutdownServer()
            self.parent().closeConnection()

    def enableUpdateBtn(self):
        self.updateBtn.setEnabled(True)

    def updateSchedulingParams(self):
        schedulingParams = {
            "cpuThreshold": self.cpuThresholdWidget.value(),
            "unusedCpuPenality": self.unusedCpuPenalityWidget.value(),
            "usableCpuBonus": self.usableCpuBonusWidget.value(),
            "unusedProgramPenality": self.unusedProgramPenalityWidget.value(),
            "cpusForUsers": self.cpusForUsersWidget.value(),
            "activeUserPenality": self.activeUserPenalityWidget.value(),
        }
        self.pySchedUI.updateSchedulingParams(schedulingParams)
        self.updateBtn.setEnabled(False)
