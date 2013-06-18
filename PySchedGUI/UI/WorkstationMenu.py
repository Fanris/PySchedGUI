# -*- coding: utf-8 -*-
'''
Created on 2013-05-23 13:23
@summary: Workstation UI
@author: predki
'''

from IMenu import IMenu

import Tables


class WorkstationMenu(IMenu):
    def __init__(self, pySchedUI):
        super(WorkstationMenu, self).__init__(pySchedUI)

    def show(self):
        print
        print "Getting Workstation informations..."
        print "================================================"
        Tables.showWSTable(self.pySchedUI)
