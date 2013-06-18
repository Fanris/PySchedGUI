# -*- coding: utf-8 -*-
'''
Created on 2013-05-23 13:36
@summary: Show Jobs UI
@author: predki
'''

from IMenu import IMenu

import CommonUI
import Tables

class GetJobsMenu(IMenu):
    def __init__(self, pySchedUI):
        super(GetJobsMenu, self).__init__(pySchedUI)

    def show(self):
        print
        print "Getting job informations..."
        print "================================================"
        archived = CommonUI.showYesNo("Show all jobs (including Archived) (y/n)? ")
        adminMode = False
        if self.pySchedUI.isAdmin:
            adminMode = CommonUI.showYesNo("(Administrator) Show Jobs of all Users (y/n)? ")

        Tables.showJobTable(self.pySchedUI, showArchived=archived, showAllUser=adminMode)
