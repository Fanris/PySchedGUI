#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-01-15 13:23
@summary:
@author: predki
'''

from PyQt4 import QtGui

from PySchedGUI.PySchedUI import PySchedUI
from PySchedGUI.GUI import GUI

import argparse
import sys

style = QtGui.QStyleFactory.create('Plastique')
QtGui.QApplication.setStyle(style)
CONST_APP = QtGui.QApplication([""])

def main():
    parser = argparse.ArgumentParser(description="PySched UI")
    parser.add_argument("-v", '--verbose', action='store_true', help="Be more verbose")
    parser.add_argument("-d", '--debug', action='store_true', help="Debug Mode")   
    parser.add_argument("-k", '--key', help="The private key file for the ssh tunnel.")
    parser.add_argument("-q", '--quiet', action='store_true', help="Be quiet")
    parser.add_argument('-u', '--user', help="The username to use for this session")
    parser.set_defaults(func=gui)  

    subparser = parser.add_subparsers(help='commands')
    guiParser = subparser.add_parser('gui', help='Starts the graphical user interface')
    guiParser.set_defaults(func=gui)
    
    addJobParser = subparser.add_parser('addjob', help='Directly schedules a Job from a template')
    addJobParser.add_argument("template", help='The job template to schedule')
    addJobParser.set_defaults(func=addJob)

    args = parser.parse_args()
    args.func(args)

def gui(args):
    pySchedUI = PySchedUI(args, cmd=None)
    mainWindow = GUI(pySchedUI)
    mainWindow.showGUI()
    sys.exit(CONST_APP.exec_())

def addJob(args):
    pass

if __name__ == "__main__":
    main()
