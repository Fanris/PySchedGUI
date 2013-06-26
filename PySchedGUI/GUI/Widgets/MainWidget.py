# -*- coding: utf-8 -*-
'''
Created on 2013-05-03 11:52
@summary: 
@author: Martin predki
'''

from PySide import QtGui, QtCore

from JobTable import JobTable
from WorkstationTable import WSTable
from PySchedGUI.GUI.Dialogs.AddJobDialog import AddJobDialog
from PySchedGUI.GUI.Dialogs.JobInfoDialog import JobInfoDialog
from PySchedGUI.GUI.Dialogs.JobFolderDialog import JobFolderDialog

from PySchedGUI.PySchedUI.DataStructures import JobState


class MainWidget(QtGui.QSplitter):    
    def __init__(self, parent=None):
        self.ui = parent.pySchedUI
        QtGui.QSplitter.__init__(self, parent)

        self.setOrientation(QtCore.Qt.Vertical)

        self.upperSplitterWidget = QtGui.QWidget()
        upperHorizontalLayout = QtGui.QHBoxLayout(self.upperSplitterWidget)        
        upperHorizontalLayout.setContentsMargins(10, 10, 10, 5)

        btnWidget = QtGui.QWidget()              
        verticalLayoutBtns = QtGui.QVBoxLayout(btnWidget)
        verticalLayoutBtns.setContentsMargins(0, 0, 0, 0)

        self.addJobBtn = QtGui.QPushButton()
        self.addJobBtn.setText("Add Job")
        self.addJobBtn.connect(self.addJobBtn, QtCore.SIGNAL("clicked()"),
            self.showAddJobDialog)
        verticalLayoutBtns.addWidget(self.addJobBtn)

        self.refreshBtn = QtGui.QPushButton()
        self.refreshBtn.setText("Refresh")
        self.refreshBtn.connect(self.refreshBtn, QtCore.SIGNAL("clicked()"),
            self.updateTables)
        verticalLayoutBtns.addWidget(self.refreshBtn)
        verticalLayoutBtns.addStretch()

        self.jobTable = JobTable(mainWidget=self)        

        self.lowerSplitterWidget = QtGui.QWidget()
        lowerHorizontalLayout = QtGui.QHBoxLayout(self.lowerSplitterWidget)        
        lowerHorizontalLayout.setContentsMargins(10, 5, 10, 10)
        self.wsTable = WSTable(mainWidget=self)

        upperHorizontalLayout.addWidget(btnWidget)
        upperHorizontalLayout.addWidget(self.jobTable)
        self.addWidget(self.upperSplitterWidget)

        lowerHorizontalLayout.addWidget(self.wsTable)
        self.addWidget(self.lowerSplitterWidget)

    def resizeEvent (self, QResizeEvent):
        if QResizeEvent.oldSize().height() == -1:
            return 
            
        s1 = self.geometry().height() * float(self.sizes()[0]) / float(QResizeEvent.oldSize().height())
        s2 = self.geometry().height() * float(self.sizes()[1]) / float(QResizeEvent.oldSize().height())

        self.setSizes([s1, s2])


    def updateTables(self):
        selectedJobs = self.jobTable.getSelectedJobs()
        selectedWs = self.wsTable.getSelectedWorkstations()

        jobs = self.ui.getJobs(archived=False, adminMode=self.parent().adminMode)
        self.jobTable.updateTable(jobs)        
        self.jobTable.selectJobIds(selectedJobs)

        ws, server = self.ui.getWorkstations()
        self.wsTable.updateTable(ws, server)
        self.wsTable.selectWorkstations(selectedWs)


    def addJobs(self, paths):
        failed = []
        for path in paths:
            if not self.ui.addJobConfigFile(path):
                failed.append(path)
        
        if len(failed) > 0:
            QtGui.QMessageBox.warning(self,
                "Errors on submitting jobs:",
                "The following jobs could not be uploaded:\n{}".format(failed),
                QtGui.QMessageBox.Ok)
        self.updateTables()

    def downloadResults(self):
        pathToSave = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory")
        
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
        jobIds = self.jobTable.getSelectedJobs()      

        self.ui.pauseJobs(jobIds)
        self.updateTables() 

    def resumeJob(self):
        selectedJobs = self.jobTable.getSelectedJobs()
        self.ui.resumeJobs(selectedJobs)
        self.updateTables()
    
    def abortJob(self):
        selectedJobs = self.jobTable.getSelectedJobs()

        self.ui.abortJobs(selectedJobs)
        self.updateTables()          

    def showAddJobDialog(self, templatePath=None):
        addJobDialog = AddJobDialog(self, templatePath)
        if addJobDialog.exec_():
            info = addJobDialog.createConfigFile()
            if not self.ui.addJob(info):
                QtGui.QMessageBox.warning(self,
                    "Errors on submitting job:",
                    "The job could not be uploaded!",
                    QtGui.QMessageBox.Ok)

        self.updateTables()

    def showJobDetails(self):
        jobIds = self.jobTable.getSelectedJobs()
        if len(jobIds) == 1:
            jobId = jobIds[0]
            jobLog = self.ui.getJobLog(jobId)
            jobLogDialog = JobInfoDialog(jobLog)
            jobLogDialog.exec_()

    def updateJob(self):
        paths = []
        for path in QtGui.QFileDialog.getOpenFileNames(self, "Select Files which will be added to the job"):
            paths.append(str(path))

        jobIds = self.jobTable.getSelectedJobs()
        if len(paths) > 0 and len(jobIds) == 1:
            self.ui.logger.debug("Updating Job...")
            if not self.ui.updateJobData(jobIds[0], paths):
                QtGui.QMessageBox.warning(self,
                    "Failure",
                    "The job could not be updated!",
                    QtGui.QMessageBox.Ok)

    def shutdownAll(self):
        if QtGui.QMessageBox.question(self, 
            "Shutting down", 
            "Are you sure, you want to shutdown the system?\nAll currently running jobs are aborted!",
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.No,
            QtGui.QMessageBox.No) == QtGui.QMessageBox.Ok:
            self.ui.shutdownAll()
            self.parent().closeConnection()

    def shutdownWS(self):
        workstations = self.wsTable.getSelectedWorkstations()
        
        if len(workstations) > 0:
            if QtGui.QMessageBox.question(self, 
                "Shutting down", 
                "Are you sure, you want to shutdown these workstations?\n{}\nAll currently running jobs are aborted!".format(workstations),
                QtGui.QMessageBox.Ok | QtGui.QMessageBox.No,
                QtGui.QMessageBox.No) == QtGui.QMessageBox.Ok:
                self.ui.shutdownWs(workstations)            

    def setMaintenanceMode(self):
        selectedWS = self.wsTable.getSelectedItems()
        wsDict = []
        for item in selectedWS:
            wsDict.append({
                "workstationName": item.getInfo("workstationName", None),
                "maintenance": not item.getInfo("maintenance", False)
                })
        self.ui.setMaintenanceMode(wsDict)

    def getFileContent(self):
        rows = self.jobTable.getSelectedRows()
        if len(rows) > 0:
            jobId = str(self.jobTable.item(rows[0], 1).text())
            jobContent = self.ui.getJobFolder(jobId)
            if not jobContent:
                return
                
            jobFolderDialog = JobFolderDialog(jobId, jobContent)
            if jobFolderDialog.exec_():
                content = self.ui.getFileContent(jobId, str(jobFolderDialog.getSelectedFile()))
                jobLogDialog = JobInfoDialog(content)
                jobLogDialog.exec_()

    def updateWorkstations(self):
        workstations = self.wsTable.getSelectedWorkstations()
        if QtGui.QMessageBox.question(self, 
            "Software update...", 
            "Are you sure, you want to update these workstations?\n{}\nAll currently running jobs are aborted!".format(workstations),
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.No,
            QtGui.QMessageBox.No) == QtGui.QMessageBox.Ok:
            self.ui.updateWorkstations(workstations)

        for ws in workstations:
            if "server" in ws.lower():
                self.parent().closeConnection()

    def restartWorkstations(self):
        workstations = self.wsTable.getSelectedWorkstations()
        if QtGui.QMessageBox.question(self, 
            "Restart workstations...", 
            "Are you sure, you want to restart these workstations?\n{}\nAll currently running jobs are aborted!".format(workstations),
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.No,
            QtGui.QMessageBox.No) == QtGui.QMessageBox.Ok:
            self.ui.restart(workstations)

        for ws in workstations:
            if "server" in ws.lower():
                self.parent().closeConnection()
