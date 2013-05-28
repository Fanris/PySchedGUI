# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Login.ui'
#
# Created: Mon May 27 14:11:57 2013
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class LoginDialog(QtGui.QDialog):
    def __init__(self, parent=None, rsa=None):
        QtGui.QDialog.__init__(self, parent)

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.resize(400, 208)
        self.setWindowTitle("Login")

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(10, 170, 380, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)

        self.formLayoutWidget = QtGui.QWidget(self)
        self.formLayoutWidget.setGeometry(QtCore.QRect(9, 9, 341, 151))

        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setRowWrapPolicy(QtGui.QFormLayout.WrapAllRows)
        self.formLayout.setMargin(0)

        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setText("User ID:")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)

        self.userIdEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.userIdEdit.setFocus()
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.userIdEdit)

        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setText("Path to RSA-Key:")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)

        self.rsaEdit = QtGui.QLineEdit(self.formLayoutWidget)
        if rsa:
            self.rsaEdit.setText(rsa)
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.rsaEdit)

        self.saveRSA = QtGui.QCheckBox(self.formLayoutWidget)
        self.saveRSA.setText("Save RSA-Key")
        if rsa:
            self.saveRSA.setChecked(True)

        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.saveRSA)

        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def getInfos(self):        
        return str(self.userIdEdit.text()), str(self.rsaEdit.text()), self.saveRSA.isChecked()
