# -*- coding: utf-8 -*-
'''
Created on 2013-05-23 13:36
@summary: Deletes a job
@author: predki
'''

from IMenu import IMenu

import CommonUI
import Tables

class DeleteJobMenu(IMenu):
    def __init__(self, pySchedUI):
        super(DeleteJobMenu, self).__init__(pySchedUI)

    def show(self):
        print
        print "Deleting Job..."
        print "================================================"
        print
        Tables.showJobTable(self.pySchedUI)
        print "Please enter the jobId"
        jobId = CommonUI.getTextInput("")
        if CommonUI.showYesNo("Are you sure that you want to delete job {}?".format(jobId)):
            if self.pySchedUI.deleteJobs([jobId]):
                print "Job deleted."
            else:
                print "Could not delete Job!"
