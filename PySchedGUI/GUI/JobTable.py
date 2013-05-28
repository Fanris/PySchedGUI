from PyQt4 import QtCore, QtGui

import Icons

class JobTable(QtGui.QTableWidget):
    def __init__(self, parent=None):
        QtGui.QTableWidget.__init__(self, parent)
        
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
            
            self.parent().addJobs(paths)
        else:
            event.ignore()

    def setHeaders(self):
        self.setColumnCount(8)
        self.setHorizontalHeaderLabels([
            "",
            "ID", 
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
            stateIdItem = QtGui.QTableWidgetItem()
            if "RUNNING" in job.get("stateId", ""):
                stateIdItem.setIcon(QtGui.QIcon(":/images/running.png"))
            elif "DONE" in job.get("stateId", ""):
                stateIdItem.setIcon(QtGui.QIcon(":/images/done.png"))
            elif "ERROR" in job.get("stateId", ""):
                stateIdItem.setIcon(QtGui.QIcon(":/images/error.png"))
            else:
                stateIdItem.setIcon(QtGui.QIcon(":/images/clock.png"))

            self.setItem(row, 0, stateIdItem)
            self.setItem(row, 1, QtGui.QTableWidgetItem(str(job.get("jobId", None))))
            self.setItem(row, 2, QtGui.QTableWidgetItem(str(job.get("jobName", None))))
            self.setItem(row, 3, QtGui.QTableWidgetItem(str(job.get("stateId", None))))
            self.setItem(row, 4, QtGui.QTableWidgetItem(str(job.get("added", None))))
            self.setItem(row, 5, QtGui.QTableWidgetItem(str(job.get("started", None))))
            self.setItem(row, 6, QtGui.QTableWidgetItem(str(job.get("finished", None))))
            self.setItem(row, 7, QtGui.QTableWidgetItem(str(job.get("workstation", None))))
            row += 1 

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        pauseJobAction = menu.addAction("Pause Job(s)")
        resumeJobAction = menu.addAction("Resume Job(s)")
        abortJobAction = menu.addAction("Abort Job(s)")
        menu.addSeparator()
        downloadResultsAction = menu.addAction("Download results...")
        menu.addSeparator()
        deleteJobAction = menu.addAction("Delete Job(s)")


        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == downloadResultsAction:
            self.parent().downloadResults()
        elif action == deleteJobAction:
            self.parent().deleteJob()
        elif action == pauseJobAction:
            self.parent().pauseJob()
        elif action == resumeJobAction:
            self.parent().resumeJob()
        elif action == abortJobAction:
            self.parent().abortJob()