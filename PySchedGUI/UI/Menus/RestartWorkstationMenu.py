# -*- coding: utf-8 -*-
'''
Created on 2013-05-23 13:36
@summary: Aborts a job
@author: predki
'''

from IMenu import IMenu

import CommonUI
import Tables

class RestartWorkstationMenu(IMenu):
    def __init__(self, pySchedUI):
        super(RestartWorkstationMenu, self).__init__(pySchedUI)

    def show(self):
        '''
        @summary: Sends a update command to the server.
        @result: 
        '''
        print
        print "Restart Workstation..."
        print "================================================"
        Tables.showWSTable(self.pySchedUI)
        print "Which workstation (name or 'server') should be restarted?"
        workstation = CommonUI.getTextInput("", "", "Please type the name of the workstation or 'server' to restart the server")
        if not workstation == "":        	
        	self.pySchedUI.restart([workstation])
