# -*- coding: utf-8 -*-
'''
Created on 2013-05-23 13:36
@summary: Aborts a job
@author: predki
'''

from IMenu import IMenu

import CommonUI

class ServerShutdownMenu(IMenu):
    def __init__(self, pySchedUI):
        super(ServerShutdownMenu, self).__init__(pySchedUI)

    def show(self):
        '''
        @summary: Sends a shutdown command to the server.
        @result: 
        '''
        if CommonUI.showYesNo("Are you sure, that you want to stop the PySched-Server? (y/n): "):
            self.pySchedUI.shutdownServer()
