# -*- coding: utf-8 -*-
'''
Created on 2013-06-10 11:55
@summary: 
@author: predki
'''
from PySide import QtGui
from PySchedGUI.GUI import Icons


class WorkstationTableItem(object):
    def __init__(self, workstationInfo):
        self.info = workstationInfo

    def addToTable(self, row, table):
        maintenance = self.info.get("maintenance", False)
        if maintenance:
            maintenanceItem = QtGui.QTableWidgetItem()
            maintenanceItem.setIcon(QtGui.QIcon(":/images/maintenanceMode.png"))
            maintenanceItem.setToolTip("This Workstation is currently in Maintenance mode and not available for new Jobs.")
            table.setItem(row, 0, maintenanceItem)

        table.setItem(row, 1, QtGui.QTableWidgetItem(str(self.info.get("workstationName", "N/A"))))
        table.setItem(row, 2, QtGui.QTableWidgetItem(str(self.info.get("version", "N/A"))))
        table.setItem(row, 3, QtGui.QTableWidgetItem(str(self.info.get("activeJobs", "N/A"))))
        table.setItem(row, 4, QtGui.QTableWidgetItem(str(self.info.get("cpuCount", "N/A"))))
        table.setItem(row, 5, QtGui.QTableWidgetItem(str(self.info.get("cpuLoad", "N/A"))))
        table.setItem(row, 6, QtGui.QTableWidgetItem(str(self.info.get("memoryLoad", "N/A"))))
        table.setItem(row, 7, QtGui.QTableWidgetItem("{}GB / {}GB ({}%)".format(
                self.info.get("diskAvailable", 0),
                self.info.get("diskFree", 0),
                100 - float(self.info.get("diskLoad", 100)))))
        table.setItem(row, 8, QtGui.QTableWidgetItem(str(self.info.get("programs", "N/A"))))
        table.setItem(row, 9, QtGui.QTableWidgetItem(str(self.info.get("machine", "N/A"))))

    def getInfo(self, info, default):
        return self.info.get(info, default)
