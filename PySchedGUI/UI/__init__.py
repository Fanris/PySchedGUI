# -*- coding: utf-8 -*-
'''
Created on 2013-01-15 11:57
@summary:
@author: Martin Predki
'''
from PathCompleter import PathCompleter

from AbortJobMenu import AbortJobMenu
from AddJobMenu import AddJobMenu
from UserMenu import UserMenu
from DeleteJobMenu import DeleteJobMenu
from GetJobsMenu import GetJobsMenu
from GetJobLogMenu import GetJobLogMenu
from GetResultsMenu import GetResultsMenu
from SearchPathMenu import SearchPathMenu
from ServerShutdownMenu import ServerShutdownMenu
from WorkstationMenu import WorkstationMenu
from PauseMenu import PauseMenu
from ResumeMenu import ResumeMenu
from UpdateMenu import UpdateMenu
from UpdateWorkstationMenu import UpdateWorkstationMenu
from RestartWorkstationMenu import RestartWorkstationMenu

import CommonUI
import readline


class UI(object):
    '''
    @summary: UI class for the PySchedUI.
    '''

    def __init__(self, pySchedUI, debug=False):
        '''
        @summary: Initializes the UI
        @param pySchedUI: a reference to the main class
        @result:
        '''
        self.pySchedUI = pySchedUI
        self.debug = debug
        self.stop = False

        completer = PathCompleter()
        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')

        self.functionList = [
            {"display": "Schedule a new Job", "function": AddJobMenu(self.pySchedUI).show},
            {"display": "Show my Jobs", "function": GetJobsMenu(self.pySchedUI).show},
            {"display": "Show Job Logfile", "function": GetJobLogMenu(self.pySchedUI).show},
            {"display": "Abort a Job", "function": AbortJobMenu(self.pySchedUI).show},
            {"display": "Update a Job", "function": UpdateMenu(self.pySchedUI).show},
            {"display": "Pause a Job", "function": PauseMenu(self.pySchedUI).show},
            {"display": "Resume a Job", "function": ResumeMenu(self.pySchedUI).show},
            {"display": "Delete a Job", "function": DeleteJobMenu(self.pySchedUI).show},
            {"display": "Get Job results", "function": GetResultsMenu(self.pySchedUI).show},
            {"display": "Get all Job results", "function": GetResultsMenu(self.pySchedUI).showGetAllResultsUI},
            {"display": "Get workstationinformations", "function": WorkstationMenu(self.pySchedUI).show},
            {"display": "Admin: Create / Edit an user", "function": UserMenu(self.pySchedUI).show, "admin": True},
            {"display": "Admin: Add Program search Path", "function": SearchPathMenu(self.pySchedUI).show, "admin": True},
            {"display": "Admin: Force scheduling", "function": self.pySchedUI.forceSchedule, "admin": True},            
            {"display": "Admin: Force Checking Jobs", "function": self.pySchedUI.checkJobs, "admin": True},       
            {"display": "Admin: Restart Workstation", "function": RestartWorkstationMenu(self.pySchedUI).show, "admin": True},   
            {"display": "Admin: Force Server shutdown", "function": ServerShutdownMenu(self.pySchedUI).show, "admin": True},
            {"display": "Admin: Update Software", "function": UpdateWorkstationMenu(self.pySchedUI).show, "admin": True},
            {"display": "Admin: Shutdown all", "function": self.pySchedUI.shutdownAll, "admin": True},
            {"display": "Quit", "function": self.close}
        ]

        print "Welcome to PySched - A python network scheduler."
        print

    # UI Functions.
    # ======================================================
    def showMainMenu(self):
        if not self.pySchedUI.userId:
            self.pySchedUI.userId = CommonUI.askForUsername()

        if not self.pySchedUI.rsaKey:
            self.pySchedUI.rsaKey = CommonUI.askForRSAKey()

        if not self.pySchedUI.openConnection():
            print "Error! Could not connect to server!"
            return

        print
        print
        print "+------------------------------------------------+"
        print "|        Welcome to the PySched UI v{}!       |".format(self.pySchedUI.version)
        print "+------------------------------------------------+"
        
        availableFunctions = {}
        while not self.stop:
            print
            if self.pySchedUI.isAdmin:
                print "Functions (Administrator):"
            else:
                print "Functions:"
            print "================================================"

            for functionIndex in range(0, len(self.functionList)):
                if not self.functionList[functionIndex].get("admin", False) or \
                    (self.pySchedUI.isAdmin and self.functionList[functionIndex].get("admin", False)):
                    
                    availableFunctions[functionIndex + 1] = self.functionList[functionIndex]["function"]
                    print "{}: {}".format(str(functionIndex + 1).rjust(2), self.functionList[functionIndex]["display"])
            print

            selected = raw_input("What do you want to do? ")

            try:
                selected = int(selected)
            except ValueError:
                selected = None

            if selected and selected in availableFunctions:
                availableFunctions[selected]()

        print "Thanks for using PySched. Bye!"

    def close(self):
        self.stop = True
