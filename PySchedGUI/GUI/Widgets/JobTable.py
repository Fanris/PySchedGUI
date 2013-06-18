from PyQt4 import QtCore, QtGui

from PySchedGUI.GUI import Icons

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
            return

        self.setRowCount(len(jobs))
        row = 0
        for job in jobs:
            try:
                stateIdItem = QtGui.QTableWidgetItem()
                if "RUNNING" in job.get("stateId", ""):
                    stateIdItem.setIcon(QtGui.QIcon(":/images/running.png"))
                elif "DONE" in job.get("stateId", ""):
                    stateIdItem.setIcon(QtGui.QIcon(":/images/done.png"))
                elif "ERROR" in job.get("stateId", "") or \
                    "ABORTED" in job.get("stateId", ""):
                    stateIdItem.setIcon(QtGui.QIcon(":/images/error.png"))
                else:
                    stateIdItem.setIcon(QtGui.QIcon(":/images/clock.png"))

                self.setItem(row, 0, stateIdItem)
            except:
                pass
                
            self.setItem(row, 1, QtGui.QTableWidgetItem(str(job.get("jobId", None))))
            self.setItem(row, 2, QtGui.QTableWidgetItem(str(job.get("userId", None))))
            self.setItem(row, 3, QtGui.QTableWidgetItem(str(job.get("jobName", None))))
            self.setItem(row, 4, QtGui.QTableWidgetItem(str(job.get("stateId", None))))
            self.setItem(row, 5, QtGui.QTableWidgetItem(str(job.get("added", None))))
            self.setItem(row, 6, QtGui.QTableWidgetItem(str(job.get("started", None))))
            self.setItem(row, 7, QtGui.QTableWidgetItem(str(job.get("finished", None))))
            self.setItem(row, 8, QtGui.QTableWidgetItem(str(job.get("workstation", None))))
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
        getFileContentAction.setEnabled(singleSelectionActionsEnabled) 

        updateJobAction = menu.addAction("Update Job")    
        updateJobAction.setEnabled(singleSelectionActionsEnabled)

        pauseJobAction = menu.addAction("Pause Job(s)")
        resumeJobAction = menu.addAction("Resume Job(s)")
        abortJobAction = menu.addAction("Abort Job(s)")
        menu.addSeparator()
        downloadResultsAction = menu.addAction("Download results...")
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
