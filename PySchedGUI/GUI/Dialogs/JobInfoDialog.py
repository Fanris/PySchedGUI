from PyQt4 import QtCore, QtGui

class JobInfoDialog(QtGui.QDialog):
    def __init__(self, jobLog, parent=None):
        QtGui.QDialog.__init__(self, parent)


        self.resize(500, 400)
        self.setWindowTitle("Job Details:")
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(10, 540, 700, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)

        textBrowser = QtGui.QTextBrowser(parent=self)
        textBrowser.setGeometry(QtCore.QRect(10, 10, 480, 350))
        textBrowser.append(jobLog)

        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
        QtCore.QMetaObject.connectSlotsByName(self)
