# -*- coding: utf-8 -*-
'''
Created on 2013-06-04 13:48
@summary: 
@author: predki
'''


from PyQt4 import QtCore, QtGui

from PySchedGUI.PySchedUI.DataStructures import User

class UserDialog(QtGui.QDialog):
    def __init__(self, parent=None, user=None):
        QtGui.QDialog.__init__(self, parent)

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.resize(400, 300)
        self.setWindowTitle("Create / Edit User")

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(10, 260, 380, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)

        self.formLayoutWidget = QtGui.QWidget(self)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 380, 240))

        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setRowWrapPolicy(QtGui.QFormLayout.WrapAllRows)
        self.formLayout.setMargin(0)

        
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setText("Email:")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)

        self.emailEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.emailEdit.setFocus()
        if user:
            self.emailEdit.setText(user.email)
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.emailEdit)

        
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setText("First Name:")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)

        self.firstNameEdit = QtGui.QLineEdit(self.formLayoutWidget)
        if user:
            self.firstNameEdit.setText(user.firstName)            
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.firstNameEdit)

        
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setText("Last Name:")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)

        self.lastNameEdit = QtGui.QLineEdit(self.formLayoutWidget)
        if user:
            self.lastNameEdit.setText(user.lastName)            
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lastNameEdit)


        self.isAdmin = QtGui.QCheckBox(self.formLayoutWidget)
        self.isAdmin.setText("Is Admin")
        if user:
            self.isAdmin.setChecked(user.admin)
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.isAdmin)

        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def getInfos(self):        
        u = User()
        u.email = str(self.emailEdit.text())
        u.firstName = str(self.firstNameEdit.text())
        u.lastName = str(self.lastNameEdit.text())
        u.admin = self.isAdmin.isChecked()
        return u
