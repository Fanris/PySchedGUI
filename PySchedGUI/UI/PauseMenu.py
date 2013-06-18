# -*- coding: utf-8 -*-
'''
Created on 2013-05-23 13:23
@summary: Retrieves results from the server
@author: predki
'''

from IMenu import IMenu

import CommonUI
import Tables


class PauseMenu(IMenu):
    def __init__(self, pySchedUI):
        super(PauseMenu, self).__init__(pySchedUI)

    def show(self):
        print
        print "Pausing Job..."
        print "================================================"
        print

        Tables.showJobTable(self.pySchedUI, stateList=["RUNNING"])
        jobId = CommonUI.getTextInput("Please enter the job id")
        self.pySchedUI.pauseJobs([jobId])
