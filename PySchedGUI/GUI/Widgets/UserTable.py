from PySide import QtGui

class UserTable(QtGui.QTableWidget):
    def __init__(self, parent=None):
        QtGui.QTableWidget.__init__(self, parent)
        
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setHighlightSections(False)

        self.verticalHeader().setVisible(False)

        self.setHeaders()

    def setHeaders(self):
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels([
            "ID", 
            "Email",
            "First Name",
            "Last Name",
            "Is Admin",
        ])

    def updateTable(self, users):
        self.clearContents()

        if not users:
            return

        self.setRowCount(len(users))
        row = 0
        for user in users:
            self.setItem(row, 0, QtGui.QTableWidgetItem(str(user.get("id", None))))
            self.setItem(row, 1, QtGui.QTableWidgetItem(str(user.get("email", None))))
            self.setItem(row, 2, QtGui.QTableWidgetItem(str(user.get("firstName", None))))
            self.setItem(row, 3, QtGui.QTableWidgetItem(str(user.get("lastName", None))))
            self.setItem(row, 4, QtGui.QTableWidgetItem(str(user.get("admin", None))))
            row += 1 

        self.horizontalHeader().resizeSections(QtGui.QHeaderView.ResizeToContents)
        
    def getSelectedRows(self):
        rows=[]
        for idx in self.selectedIndexes():
            if not idx.row() in rows:
                rows.append(idx.row())  
        return rows
