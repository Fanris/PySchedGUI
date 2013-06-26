#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-01-15 13:23
@summary:
@author: predki
'''

from PySide import QtGui

from PySchedGUI.PySchedUI import PySchedUI
from PySchedGUI.GUI import GUI
from PySchedGUI.UI import UI

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="PySched UI")
    parser.add_argument("-v", '--verbose', action='store_true', help="Be more verbose")
    parser.add_argument("-d", '--debug', action='store_true', help="Debug Mode")   
    parser.add_argument("-k", '--key', help="The private key file for the ssh tunnel.")
    parser.add_argument("-q", '--quiet', action='store_true', help="Be quiet")
    parser.add_argument('-u', '--user', help="The username to use for this session")
    parser.add_argument('-m', '--multicast', help="A Multicast group on which the GUI should listen for a server")
    parser.add_argument('-s', '--server', help="The Server to connect to. (This disables the automatic search for a server!)")

    subparser = parser.add_subparsers(help='commands')

    uiParser = subparser.add_parser('ui', help='Starts the console based user interface')
    uiParser.set_defaults(func=ui)

    guiParser = subparser.add_parser('gui', help='Starts the graphical user interface')
    guiParser.set_defaults(func=gui)
    
    addJobParser = subparser.add_parser('addjob', help='Directly schedules a Job from a template')
    addJobParser.add_argument("template", help='The job template to schedule')
    addJobParser.set_defaults(func=addJob)

    args = parser.parse_args()
    args.func(args)

def gui(args):
    QtGui.QApplication.setStyle('Plastique')
    CONST_APP = QtGui.QApplication([""])    

    pySchedUI = PySchedUI(args, cmd=None)
    mainWindow = GUI(pySchedUI)
    
    mainWindow.showGUI()
    sys.exit(CONST_APP.exec_())    

def addJob(args):
    PySchedUI(args, cmd="addJob")

def gui(args):
    try:
        QtGui.QApplication.setStyle('Plastique')
        CONST_APP = QtGui.QApplication([""])

        pySchedUI = PySchedUI(args, cmd=None)
        mainWindow = GUI(pySchedUI)
        
        mainWindow.showGUI()
        CONST_APP.exec_()
        mainWindow.exit()
        
        sys.exit()
    except:
        pass

def ui(args):
    pySchedUI = PySchedUI(args, cmd=None)
    ui = UI(pySchedUI)
    ui.showMainMenu()

if __name__ == "__main__":
    main()
