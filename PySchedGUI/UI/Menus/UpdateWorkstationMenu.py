# -*- coding: utf-8 -*-
'''
Created on 2013-05-23 13:36
@summary: Aborts a job
@author: predki
'''

from IMenu import IMenu

import CommonUI
import Tables

class UpdateWorkstationMenu(IMenu):
    def __init__(self, pySchedUI):
        super(UpdateWorkstationMenu, self).__init__(pySchedUI)

    def show(self):
        '''
        @summary: Sends a update command to the server.
        @result: 
        '''
        print
        print "Getting Workstation informations..."
        print "================================================"
        Tables.showWSTable(self.pySchedUI)
        print "Which workstation (name or 'server') should be updated?"
        workstation = CommonUI.getTextInput("", "", "Please type the name of the workstation or 'server' to update the server")
        if not workstation == "":        	
        	self.pySchedUI.updateWorkstations([workstation])

