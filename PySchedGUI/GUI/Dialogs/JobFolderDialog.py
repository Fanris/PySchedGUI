# -*- coding: utf-8 -*-
'''
Created on 2013-06-12 13:02
@summary: 
@author: predki
'''

from PySide import QtCore, QtGui

import os

class JobFolderDialog(QtGui.QDialog):
    def __init__(self, jobId, content, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.content = content

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.resize(550, 400)
        self.setWindowTitle("Job {} Folder".format(jobId))

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(10, 360, 530, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)

        self.treeView = QtGui.QTreeWidget(self)
        self.treeView.setGeometry(QtCore.QRect(10, 10, 110, 340))
        QtCore.QObject.connect(self.treeView, QtCore.SIGNAL("currentItemChanged (QTreeWidgetItem *,QTreeWidgetItem *)"), self.updateList)

        self.listView = QtGui.QListWidget(self)
        self.listView.setGeometry(QtCore.QRect(130, 10, 400, 340))

        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.updateTree(content)

    def updateTree(self, content):
        self.treeView.setHeaderLabel("")
        rootItem = QtGui.QTreeWidgetItem()
        rootItem.setText(0, "/")        
        self.treeView.addTopLevelItem(rootItem)

        for f in content:
            if f.endswith(os.sep):
                treeItem = QtGui.QTreeWidgetItem()
                treeItem.setText(0, f)
                rootItem.addChild(treeItem)

        rootItem.setExpanded(True)

    def updateList(self):
        self.listView.clear()
        for f in self.content:
            fName = os.path.split(f)[1]
            if not fName == "":
                listItem = QtGui.QListWidgetItem(fName)
            
                if self.treeView.currentItem().text(0) == "/":
                    if "/" in f:
                        continue                

                elif not self.treeView.currentItem().text(0) in f:
                    continue

                self.listView.addItem(listItem)

        self.listView.sortItems()

    def getSelectedFile(self):
        selectedItem = self.listView.currentItem()
        selectedFolder = self.treeView.currentItem()

        if selectedItem and selectedFolder:
            path = selectedItem.text()
            curFolder = selectedFolder
            while curFolder and not curFolder.text(0) == "/":
                path = curFolder.text(0) + path
                curFolder = curFolder.parent()

            return path
