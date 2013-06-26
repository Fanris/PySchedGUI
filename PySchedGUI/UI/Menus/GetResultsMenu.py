# -*- coding: utf-8 -*-
'''
Created on 2013-05-23 13:23
@summary: Retrieves results from the server
@author: predki
'''

from IMenu import IMenu
from PySchedGUI.PySchedUI import FileUtils

import Tables
import CommonUI

class GetResultsMenu(IMenu):
    def __init__(self, pySchedUI):
        super(GetResultsMenu, self).__init__(pySchedUI)

    def show(self):
        endStates = [
             "DONE",
             "ABORTED",
             "SCHEDULER_ERROR",
             "COMPILER_ERROR",
             "WORKSTATION_ERROR",
             "PERMISSION_DENIED",
             "ERROR",
        ]

        print
        print "Getting Job results..."
        print "================================================"
        print
        Tables.showJobTable(self.pySchedUI, stateList=endStates)
        jobId = CommonUI.getTextInput("Please enter the job id")
        path = CommonUI.getPathInput("Please select a path where the results should be stored")

        if not FileUtils.pathExists(path):
            print "Path {} does not exists! Would you like to create it? (y/n)".format(path)
            if CommonUI.showYesNo("> "):
                FileUtils.createDirectory(path)
            else:
                return

            if self.pySchedUI.getResultsByJobId([jobId], path):
                print "Results stored in {}".format(path)
            else:
                print "Could not retrieve the results of job {}".format(jobId)

    def showGetAllResultsUI(self):
        print
        print "Getting all Job results..."
        print "================================================"
        print
        path = CommonUI.getTextInput("Please select a path where the results should be stored: ")
        self.pySchedUI.getAllResults(path)
