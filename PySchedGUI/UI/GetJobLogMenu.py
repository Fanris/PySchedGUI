# -*- coding: utf-8 -*-
'''
Created on 2013-05-23 13:36
@summary: Retrieves the jobs log file
@author: predki
'''

from IMenu import IMenu

import CommonUI
import Tables

class GetJobLogMenu(IMenu):
    def __init__(self, pySchedUI):
        super(GetJobLogMenu, self).__init__(pySchedUI)

    def show(self):
        print
        print "Getting job log file..."
        print "================================================"

        showAll = False
        if self.pySchedUI.isAdmin:
            showAll = CommonUI.showYesNo("(Administrator) Show Jobs of all Users (y/n)? ")

        Tables.showJobTable(self.pySchedUI, showAllUser=showAll) 
        jobId = CommonUI.getTextInput("Please enter the job id")
        print self.pySchedUI.getJobLog(jobId)    	
