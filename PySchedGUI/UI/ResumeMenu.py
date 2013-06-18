# -*- coding: utf-8 -*-
'''
Created on 2013-05-23 13:23
@summary: Retrieves results from the server
@author: predki
'''

from IMenu import IMenu

import CommonUI
import Tables


class ResumeMenu(IMenu):
    def __init__(self, pySchedUI):
        super(ResumeMenu, self).__init__(pySchedUI)

    def show(self):
        print
        print "Pausing Job..."
        print "================================================"
        print
        Tables.showJobTable(self.pySchedUI, stateList=["PAUSED"])
        jobId = CommonUI.getTextInput("")
        self.pySchedUI.resumeJobs([jobId])
