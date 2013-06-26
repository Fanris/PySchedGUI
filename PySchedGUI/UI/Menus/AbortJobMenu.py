# -*- coding: utf-8 -*-
'''
Created on 2013-05-23 13:36
@summary: Aborts a job
@author: predki
'''

from IMenu import IMenu
import CommonUI

import Tables

class AbortJobMenu(IMenu):
    def __init__(self, pySchedUI):
        super(AbortJobMenu, self).__init__(pySchedUI)

    def show(self):
        print
        print "Aborting Job..."
        print "================================================"
        print
        Tables.showJobTable(self.pySchedUI)
        print
        jobId = CommonUI.getTextInput("Please enter the job id")
        if self.pySchedUI.abortJobs([jobId]):
            print "Job {} aborted.".format(jobId)
        else:
            print "Could not abort the job."
