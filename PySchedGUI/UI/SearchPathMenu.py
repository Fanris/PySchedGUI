# -*- coding: utf-8 -*-
'''
Created on 2013-05-23 13:23
@summary: Search path UI
'''

from IMenu import IMenu
from PySchedGUI.PySchedUI.UIDict import UIDict


class SearchPathMenu(IMenu):
    def __init__(self, pySchedUI):
        super(SearchPathMenu, self).__init__(pySchedUI)

    def show(self):
        inp = UIDict()
        print
        print "Update Program Search Paths..."
        print "================================================"
        print

        paths = self.pySchedUI.getPaths(inp.getInfos())
        if paths and len(paths) > 0:
            print "Current search paths:"    
            for p in paths:
                print p

        print "Please give the new path to add"
        inp.addInfo("Path", "path", raw_input("> "))
        self.pySchedUI.addSearchPath(inp.getInfos())
