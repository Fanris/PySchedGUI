# -*- coding: utf-8 -*-
'''
Created on 2013-06-10 11:55
@summary: 
@author: predki
'''

from PyQt4 import QtGui
from PySchedGUI.GUI import Icons

class JobTableItem(object):
    def __init__(self, jobInfo):
        self.info = jobInfo

    def addToTable(self, row, table):
            try:
                stateIdItem = QtGui.QTableWidgetItem()
                if "RUNNING" in self.info.get("stateId", ""):
                    stateIdItem.setIcon(QtGui.QIcon(":/images/running.png"))
                elif "DONE" in self.info.get("stateId", ""):
                    stateIdItem.setIcon(QtGui.QIcon(":/images/done.png"))
                elif "ERROR" in self.info.get("stateId", "") or \
                    "ABORTED" in self.info.get("stateId", ""):
                    stateIdItem.setIcon(QtGui.QIcon(":/images/error.png"))
                else:
                    stateIdItem.setIcon(QtGui.QIcon(":/images/clock.png"))

                table.setItem(row, 0, stateIdItem)
            except:
                pass
                
            table.setItem(row, 1, QtGui.QTableWidgetItem(str(self.info.get("jobId", None))))
            table.setItem(row, 2, QtGui.QTableWidgetItem(str(self.info.get("userId", None))))
            table.setItem(row, 3, QtGui.QTableWidgetItem(str(self.info.get("jobName", None))))
            table.setItem(row, 4, QtGui.QTableWidgetItem(str(self.info.get("stateId", None))))
            table.setItem(row, 5, QtGui.QTableWidgetItem(str(self.info.get("added", None))))
            table.setItem(row, 6, QtGui.QTableWidgetItem(str(self.info.get("started", None))))
            table.setItem(row, 7, QtGui.QTableWidgetItem(str(self.info.get("finished", None))))
            table.setItem(row, 8, QtGui.QTableWidgetItem(str(self.info.get("workstation", None))))

    def getInfo(self, info, default):
        return self.info.get(info, default)
