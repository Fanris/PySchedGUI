#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-01-15 13:23
@summary:
@author: predki
'''

from PySchedGUI.PySchedUI import PySchedUI
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
    
    addJobParser = subparser.add_parser('addjob', help='Directly schedules a Job from a template')
    addJobParser.add_argument("template", help='The job template to schedule')
    addJobParser.set_defaults(func=addJob)

    args = parser.parse_args()
    args.func(args)   

def addJob(args):
    PySchedUI(args, cmd="addJob")

def ui(args):
    pySchedUI = PySchedUI(args, cmd=None)
    ui = UI(pySchedUI)
    ui.showMainMenu()

if __name__ == "__main__":
    main()
