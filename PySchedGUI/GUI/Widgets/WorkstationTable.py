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
        menu = QtGui.QMenu(self)

        shutdownAllAction = menu.addAction("Shutdown all")
        shutdownAllAction.setEnabled(self.parent().ui.isAdmin)

        shutdownWSAction = menu.addAction("Shutdown Workstation(s)")    
        shutdownWSAction.setEnabled(self.parent().ui.isAdmin)


        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == shutdownWSAction:
            self.parent().shutdownWS()            
        elif action == shutdownAllAction:
            self.parent().shutdownAll()

    def getSelectedRows(self):
        rows=[]
        for idx in self.selectedIndexes():
            if not idx.row() in rows:
                rows.append(idx.row())  
        return rows
