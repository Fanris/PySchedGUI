from PyQt4 import QtGui

from WorkstationTableItem import WorkstationTableItem

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
        self.currentItems = []

    def setHeaders(self):
        self.setColumnCount(10)
        self.setHorizontalHeaderLabels([
            "",
            "Machine Name", 
            "Version",
            "Active Jobs",
            "CPU Count",
            "CPU Load",
            "Memory Load",
            "Disk (Available / Free)",
            "Programs",
            "Machine",
            "Maintenance"])

    def updateTable(self, workstations, server):
        self.clearContents()
        self.currentItems = []       
        row = 0

        if not workstations and not server:
            return

        if server:
            workstations.insert(0, server)

        self.setRowCount(len(workstations))

        for workstation in workstations:
            wsItem = WorkstationTableItem(workstation)
            wsItem.addToTable(row, self)
            self.currentItems.append(wsItem)
            row += 1


        self.horizontalHeader().resizeSections(QtGui.QHeaderView.ResizeToContents)

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)

        maintenanceAction = menu.addAction("(De)Activate Maintenance Mode")
        maintenanceAction.setEnabled(self.parent().ui.isAdmin)

        menu.addSeparator()

        shutdownAllAction = menu.addAction("Shutdown all")
        shutdownAllAction.setEnabled(self.parent().ui.isAdmin)

        shutdownWSAction = menu.addAction("Shutdown Workstation(s)")    
        shutdownWSAction.setEnabled(self.parent().ui.isAdmin)


        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == shutdownWSAction:
            self.parent().shutdownWS()            
        elif action == shutdownAllAction:
            self.parent().shutdownAll()
        elif action == maintenanceAction:
            self.parent().setMaintenanceMode()

    def getSelectedRows(self):
        rows=[]
        for idx in self.selectedIndexes():
            if not idx.row() in rows:
                rows.append(idx.row())  
        return rows

    def getSelectedItems(self):
        rows = self.getSelectedRows()
        items = []
        for index in rows:
            items.append(self.currentItems[index])
        return items
