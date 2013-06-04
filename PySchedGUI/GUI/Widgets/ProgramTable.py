from PyQt4 import QtCore, QtGui

class ProgramTable(QtGui.QTableWidget):
    def __init__(self, parent=None):
        QtGui.QTableWidget.__init__(self, parent)
        
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setHighlightSections(False)

        self.verticalHeader().setVisible(False)

        self.setHeaders()

    def setHeaders(self):
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels([
            "ID", 
            "Program Name",
            "Program Path",
            "Program Exec",
            "Program Version",        
        ])

    def updateTable(self, programs):
        self.clearContents()

        if not programs:
            return

        self.setRowCount(len(programs))
        row = 0
        for program in programs:
            self.setItem(row, 0, QtGui.QTableWidgetItem(str(program.get("id", None))))
            self.setItem(row, 1, QtGui.QTableWidgetItem(str(program.get("programName", None))))
            self.setItem(row, 2, QtGui.QTableWidgetItem(str(program.get("programPath", None))))
            self.setItem(row, 3, QtGui.QTableWidgetItem(str(program.get("programExec", None))))
            self.setItem(row, 4, QtGui.QTableWidgetItem(str(program.get("programVersion", None))))
            row += 1 

        self.horizontalHeader().resizeSections(QtGui.QHeaderView.ResizeToContents)

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        deleteJobAction = menu.addAction("Delete User(s)")


        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == deleteJobAction:
            self.parent().deleteJob()

