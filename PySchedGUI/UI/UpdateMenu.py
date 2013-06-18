# -*- coding: utf-8 -*-
'''
Created on 2013-05-23 13:23
@summary: Add Job Menu
@author: predki
'''

from IMenu import IMenu
from PySchedGUI.PySchedUI.UIDict import UIDict

import Tables
import CommonUI


class UpdateMenu(IMenu):
    def __init__(self, pySchedUI):
        super(UpdateMenu, self).__init__(pySchedUI)

    def show(self):
        newInp = UIDict()
        updateableStates = [
            "RUNNING",
            "PAUSED"
        ]
        print
        print "Updating Job data..."
        print "================================================"
        print        
        Tables.showJobTable(self.pySchedUI, stateList=updateableStates)
        jobId = CommonUI.getTextInput("Please enter the job id")

        print
        print "Please specify which files should be transferred to the server."
        print "Enter nothing to to move on, '?' for help"
        paths = []
        tmp = CommonUI.getPathInput("", "", help=PATH_HELP)
        while tmp != "":
            paths.append(tmp)
            newInp.addInfo("Copy Paths", "paths", paths)
            tmp = CommonUI.getTextInput("", "", help=PATH_HELP)

        self.pySchedUI.updateJobData(jobId, paths)


PATH_HELP = """
This section defines the files that are needed by the program.
All files specified here are send to the server. If a folder is
specified the content will be send to the server.

Examples:
/home/user/HelloWorld.c will send the file HelloWorld.c to the server
/home/user/foo/ will send the complete folder to the server
/home/user/foo/* will send the content of the folder foo to the server"""
