from PyQt4 import QtCore, QtGui

from JobTableItem import JobTableItem

class JobTable(QtGui.QTableWidget):
    def __init__(self, mainWidget, parent=None):
        QtGui.QTableWidget.__init__(self, parent)
        self.mainWidget = mainWidget

        self.setAcceptDrops(True)
        self.setDragDropMode(QtGui.QAbstractItemView.DropOnly)
        self.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setHighlightSections(False)

        self.verticalHeader().setVisible(False)

        self.setHeaders()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            paths = []
            for url in event.mimeData().urls():
                paths.append(str(url.toLocalFile()))
            
            self.mainWidget.addJobs(paths)
        else:
            event.ignore()

    def setHeaders(self):
        self.setColumnCount(9)
        self.setHorizontalHeaderLabels([
            "",
            "ID", 
            "User",
            "Name",
            "Status",
            "Added",
            "Started",
            "Ended",
            "Workstation"])

    def updateTable(self, jobs):
        self.clearContents()

        if not jobs:
            self.setRowCount(0)
            return

        self.setRowCount(len(jobs))
        row = 0
        for job in jobs:
            jobItem = JobTableItem(job)
            jobItem.addToTable(row, self)

            row += 1

        self.horizontalHeader().resizeSections(QtGui.QHeaderView.ResizeToContents)

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)

        singleSelectionActionsEnabled = True
        rows = self.getSelectedRows()
        if len(rows) > 1:
            singleSelectionActionsEnabled = False    

        showJobDetailsAction = menu.addAction("Show Job Details")        
        showJobDetailsAction.setEnabled(singleSelectionActionsEnabled)
        menu.addSeparator()        

        getFileContentAction = menu.addAction("Get File")
        if singleSelectionActionsEnabled and \
            self.getItemText(rows[0], 4) in ["RUNNING", "PAUSED"]:
            getFileContentAction.setEnabled(singleSelectionActionsEnabled)
        else:
            getFileContentAction.setEnabled(False)

        updateJobAction = menu.addAction("Update Job")    
        if singleSelectionActionsEnabled and \
            self.getItemText(rows[0], 4) in ["RUNNING", "PAUSED"]:
            updateJobAction.setEnabled(singleSelectionActionsEnabled)
        else:
            updateJobAction.setEnabled(False)

        pauseJobAction = menu.addAction("Pause Job(s)")
        if self.getItemText(rows[0], 4) in ["RUNNING"]:
            pauseJobAction.setEnabled(True)
        else:
            pauseJobAction.setEnabled(False)

        resumeJobAction = menu.addAction("Resume Job(s)")
        if self.getItemText(rows[0], 4) in ["PAUSED"]:
            resumeJobAction.setEnabled(True)
        else:
            resumeJobAction.setEnabled(False)

        abortJobAction = menu.addAction("Abort Job(s)")
        if self.getItemText(rows[0], 4) in ["RUNNING", "PAUSED"]:
            abortJobAction.setEnabled(True)
        else:
            abortJobAction.setEnabled(False)

        menu.addSeparator()
        downloadResultsAction = menu.addAction("Download results...")
        if self.getItemText(rows[0], 4) not in \
                ["RUNNING", "PAUSED", "COMPILED", "PREPARED", "DISPATCHED", "WAITING_FOR_WORKSTATION"]:
            downloadResultsAction.setEnabled(True)
        else:
            downloadResultsAction.setEnabled(False)

        menu.addSeparator()
        deleteJobAction = menu.addAction("Delete Job(s)")


        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == downloadResultsAction:
            self.mainWidget.downloadResults()
        elif action == deleteJobAction:
            self.mainWidget.deleteJob()
        elif action == pauseJobAction:
            self.mainWidget.pauseJob()
        elif action == resumeJobAction:
            self.mainWidget.resumeJob()
        elif action == abortJobAction:
            self.mainWidget.abortJob()
        elif action == updateJobAction:
            self.mainWidget.updateJob()
        elif action == showJobDetailsAction:
            self.mainWidget.showJobDetails()
        elif action == getFileContentAction:
            self.mainWidget.getFileContent()

    def getSelectedRows(self):
        rows=[]
        for idx in self.selectedIndexes():
            if not idx.row() in rows:
                rows.append(idx.row())  
        return rows

    def getItemText(self, row, column):
        return self.item(row, column).text()

    def getSelectedJobs(self):
        jobIds = []
        selectedRows = self.getSelectedRows()
        for row in selectedRows:
            itemWidget = self.item(row, 1)
            if not itemWidget:
                continue

            jobIds.append(str(self.getItemText(row, 1)))

        return jobIds

    def selectJobIds(self, jobIds):
        for index in range(0, self.rowCount()):
            itemWidget = self.item(index, 1)
            if not itemWidget:
                continue

            jobId = itemWidget.text()
            if jobId in jobIds:
                self.setRangeSelected(QtGui.QTableWidgetSelectionRange(
                    index, 0, index, 8), True)
