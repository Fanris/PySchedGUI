# -*- coding: utf-8 -*-
'''
Created on 2013-06-04 13:48
@summary: 
@author: predki
'''


from PySide import QtCore, QtGui

from PySchedGUI.PySchedUI.DataStructures import Program

class ProgramDialog(QtGui.QDialog):
    def __init__(self, parent=None, program=None):
        QtGui.QDialog.__init__(self, parent)

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.resize(400, 300)
        self.setWindowTitle("Create / Edit Program")

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(10, 260, 380, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)

        self.formLayoutWidget = QtGui.QWidget(self)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 380, 240))

        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setRowWrapPolicy(QtGui.QFormLayout.WrapAllRows)
        self.formLayout.setContentsMargins(0, 0, 0, 0)

        
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setText("Program Name:")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)

        self.programNameEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.programNameEdit.setFocus()
        if program:
            self.programNameEdit.setText(program.programName)
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.programNameEdit)

        
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setText("Program Path:")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)

        self.programPathEdit = QtGui.QLineEdit(self.formLayoutWidget)
        if program:
            self.programPathEdit.setText(program.programPath)            
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.programPathEdit)

        
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setText("Program Executable:")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)

        self.programExecEdit = QtGui.QLineEdit(self.formLayoutWidget)
        if program:
            self.programExecEdit.setText(program.programExec)            
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.programExecEdit)


        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setText("Program Version:")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_4)

        self.programVersionEdit = QtGui.QLineEdit(self.formLayoutWidget)
        if program:
            self.programVersionEdit.setText(program.programVersion)            
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.programVersionEdit)

        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def getInfos(self):        
        p = Program()
        p.programName = str(self.programNameEdit.text())
        p.programPath = str(self.programPathEdit.text())
        p.programExec = str(self.programExecEdit.text())
        p.programVersion = str(self.programVersionEdit.text())
        return p
