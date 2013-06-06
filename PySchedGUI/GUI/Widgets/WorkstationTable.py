from PyQt4 import QtGui

class WSTable(QtGui.QTableWidget):
    def __init__(self, parent=None):
        QtGui.QTableWidget.__init__(self, parent)
        
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.horizontalHeader().setHighlightSections(False)
        self.horizontalHeader().setCascadingSectionResizes(True)
        self.horizontalHeader().setStretchLastSection(True)

        self.setHeaders()

    def setHeaders(self):
        self.setColumnCount(9)
        self.setHorizontalHeaderLabels([
            "Machine Name", 
            "Version",
            "Active Jobs",
            "CPU Count",
            "CPU Load",
            "Memory Load",
            "Disk (Available / Free)",
            "Programs",
            "Machine"])

    def updateTable(self, workstations, server):
        self.clearContents()        
        row = 0

        if not workstations and not server:
            return

        if server:
            workstations.insert(0, server)

        self.setRowCount(len(workstations))

        for workstation in workstations:
            self.setItem(row, 0, QtGui.QTableWidgetItem(str(workstation.get("workstationName", "N/A"))))
            self.setItem(row, 1, QtGui.QTableWidgetItem(str(workstation.get("version", "N/A"))))
            self.setItem(row, 2, QtGui.QTableWidgetItem(str(workstation.get("activeJobs", "N/A"))))
            self.setItem(row, 3, QtGui.QTableWidgetItem(str(workstation.get("cpuCount", "N/A"))))
            self.setItem(row, 4, QtGui.QTableWidgetItem(str(workstation.get("cpuLoad", "N/A"))))
            self.setItem(row, 5, QtGui.QTableWidgetItem(str(workstation.get("memoryLoad", "N/A"))))
            self.setItem(row, 6, QtGui.QTableWidgetItem("{}GB / {}GB ({}%)".format(
                    workstation.get("diskAvailable", 0),
                    workstation.get("diskFree", 0),
                    100 - float(workstation.get("diskLoad", 100)))))
            self.setItem(row, 7, QtGui.QTableWidgetItem(str(workstation.get("programs", "N/A"))))
            self.setItem(row, 8, QtGui.QTableWidgetItem(str(workstation.get("machine", "N/A"))))
            row += 1    

        self.horizontalHeader().resizeSections(QtGui.QHeaderView.ResizeToContents)

    def contextMenuEvent(self, event):
        pass
            # menu = QtGui.QMenu(self)

            # singleSelectionActionsEnabled = True
            # rows = self.getSelectedRows()
            # if len(rows) > 1:
            #     singleSelectionActionsEnabled = False

            # showJobDetailsAction = menu.addAction("Show Job Details")
            # showJobDetailsAction.setEnabled(singleSelectionActionsEnabled)
            # menu.addSeparator()

            # updateJobAction = menu.addAction("Update Job")    
            # updateJobAction.setEnabled(singleSelectionActionsEnabled)

            # pauseJobAction = menu.addAction("Pause Job(s)")
            # resumeJobAction = menu.addAction("Resume Job(s)")
            # abortJobAction = menu.addAction("Abort Job(s)")
            # menu.addSeparator()
            # downloadResultsAction = menu.addAction("Download results...")
            # menu.addSeparator()
            # deleteJobAction = menu.addAction("Delete Job(s)")


            # action = menu.exec_(self.mapToGlobal(event.pos()))
            # if action == downloadResultsAction:
            #     self.parent().downloadResults()
            # elif action == deleteJobAction:
            #     self.parent().deleteJob()
            # elif action == pauseJobAction:
            #     self.parent().pauseJob()
            # elif action == resumeJobAction:
            #     self.parent().resumeJob()
            # elif action == abortJobAction:
            #     self.parent().abortJob()
            # elif action == updateJobAction:
            #     pass
            # elif action == showJobDetailsAction:
            #     self.parent().showJobDetails()

    def getSelectedRows(self):
        rows=[]
        for idx in self.selectedIndexes():
            if not idx.row() in rows:
                rows.append(idx.row())  
        return rows
