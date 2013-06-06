# -*- coding: utf-8 -*-
'''
Created on 2013-05-03 11:52
@summary: 
@author: Martin predki
'''

from PyQt4 import QtGui, QtCore

from JobTable import JobTable
from WorkstationTable import WSTable
from PySchedGUI.GUI.Dialogs.AddJobDialog import AddJobDialog
from PySchedGUI.GUI.Dialogs.JobInfoDialog import JobInfoDialog

from PySchedGUI.PySchedUI.DataStructures import JobState


class MainWidget(QtGui.QWidget):    
    def __init__(self, parent=None):
        self.ui = parent.pySchedUI
        QtGui.QWidget.__init__(self, parent)

        self.verticalLayoutWidget = QtGui.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 110, 80))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)

        self.addJobBtn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.addJobBtn.setText("Add Job")
        self.addJobBtn.connect(self.addJobBtn, QtCore.SIGNAL("clicked()"),
            self.showAddJobDialog)
        self.verticalLayout.addWidget(self.addJobBtn)

        self.refreshBtn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.refreshBtn.setText("Refresh")
        self.refreshBtn.connect(self.refreshBtn, QtCore.SIGNAL("clicked()"),
            self.updateTables)
        self.verticalLayout.addWidget(self.refreshBtn)

        self.jobTable = JobTable(self)
        self.jobTable.setGeometry(QtCore.QRect(130, 10, 860, 415))

        self.wsTable = WSTable(self)
        self.wsTable.setGeometry(QtCore.QRect(10, 435, 990, 155))

    def resizeEvent (self, QResizeEvent):
        jobTableWidth = self.geometry().width() - 140
        jobTableHeight = self.geometry().height() * 0.75 - 15
        self.jobTable.setGeometry(130, 10, 
            jobTableWidth, 
            jobTableHeight)

        wsTableWidth = self.geometry().width() - 20
        wsTableTop = self.geometry().height() * 0.75 + 5
        wsTableHeight = self.geometry().height() * 0.25 - 10
        self.wsTable.setGeometry(10, 
            wsTableTop,
            wsTableWidth,
            wsTableHeight)

    def updateTables(self):
        jobs = self.ui.getJobs(archived=False, adminMode=self.parent().adminMode)
        self.jobTable.updateTable(jobs)

        ws, server = self.ui.getWorkstations()
        self.wsTable.updateTable(ws, server)

    def addJobs(self, paths):
        self.ui.addJobConfigFiles(paths)
        self.updateTables()

    def downloadResults(self):
        pathToSave = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))

        self.parent().pySchedUI.logger.debug("Selected folder: {}".format(pathToSave))
        if not pathToSave:
            return
        rows = self.jobTable.getSelectedRows()         

        selectedJobs = []
        for row in rows:
            jobId = str(self.jobTable.item(row, 1).text())
            jobState = str(self.jobTable.item(row, 4).text())
            if JobState.lookup(jobState) >= JobState.lookup("DONE") and \
                JobState.lookup(jobState) <= JobState.lookup("SCHEDULER_ERROR"):
                selectedJobs.append(jobId)
            else:
                self.ui.logger.debug("JobState {} not valid for download".format(jobState))

        self.parent().pySchedUI.logger.debug("Selected jobs: {}".format(selectedJobs))
        self.ui.getResultsByJobId(selectedJobs, pathToSave)        
        self.updateTables()

    def deleteJob(self):
        rows = self.jobTable.getSelectedRows()         

        selectedJobs = []
        for row in rows:
            jobId = str(self.jobTable.item(row, 1).text())
            selectedJobs.append(jobId)

        if QtGui.QMessageBox.question(self, 
            "Deleting items...", 
            "Are you sure you want to delete the selected items?",
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.No,
            QtGui.QMessageBox.No) == QtGui.QMessageBox.Ok:
            self.ui.deleteJobs(selectedJobs)
            self.updateTables()

    def pauseJob(self):
        rows = self.jobTable.getSelectedRows()      

        selectedJobs = []
        for row in rows:
            jobId = str(self.jobTable.item(row, 1).text())
            jobState = str(self.jobTable.item(row, 3).text())
            if jobState in ["RUNNING"]:
                selectedJobs.append(jobId)

        self.ui.pauseJobs(selectedJobs)
        self.updateTables() 

    def resumeJob(self):
        rows = self.jobTable.getSelectedRows()

        selectedJobs = []
        for row in rows:
            jobId = str(self.jobTable.item(row, 1).text())
            jobState = str(self.jobTable.item(row, 3).text())
            if jobState in ["PAUSED"]:
                selectedJobs.append(jobId)

        self.ui.resumeJobs(selectedJobs)
        self.updateTables()
    
    def abortJob(self):
        rows = self.jobTable.getSelectedRows()         

        selectedJobs = []
        for row in rows:
            jobId = str(self.jobTable.item(row, 1).text())
            selectedJobs.append(jobId)

        self.ui.abortJobs(selectedJobs)
        self.updateTables()          

    def showAddJobDialog(self, templatePath=None):
        addJobDialog = AddJobDialog(self, templatePath)
        if addJobDialog.exec_():
                info = addJobDialog.createConfigFile()
                self.ui.addJob(info)

        self.updateTables()

    def showJobDetails(self):
        rows = self.jobTable.getSelectedRows()
        if len(rows) > 0:
            jobId = str(self.jobTable.item(rows[0], 1).text())
            jobLog = self.ui.getJobLog(jobId)
            jobLogDialog = JobInfoDialog(jobLog)
            jobLogDialog.exec_()
