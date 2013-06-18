# -*- coding: utf-8 -*-
'''
Created on 2013-05-23 13:16
@summary: Common UI Dialogs
@author: predki
'''

import sys
from PySchedGUI.PySchedUI import FileUtils

def showValidatingInput(inp):
    print
    print "Validating input..."
    print "================================================"
    print
    for k, v in inp.getInfos().iteritems():
        print "{key}: \t\t{value}".format(key=inp.getScreenName(k), value=v)

    return showYesNo("Are these values correct? (y / n): ")

def showYesNo(message):
    answer = raw_input(message)
    if answer.lower() == "y":
        return True
    else:
        return False

def getTextInput(text, default=None, help=None):
    inp = raw_input(text + '> ')
    while inp == "?":
        if help:
            print help
        inp = raw_input(text + '> ')

    if inp == "" and default:
        return default

    return inp.strip()

def getIntInput(text, default=None, help=None):
    inp = raw_input(text + '> ')
    while inp == "?":
        if help:
            print help
        inp = raw_input(text + '> ')

    if inp == "" and default:
        return default
    
    try:
        inp = int(inp)
    except ValueError:
        inp = default

    return inp

def getPathInput(text, default=None, help=None):
    path = raw_input(text + "> ")
    path = FileUtils.expandPath(path)

    if not path or path == "" and default:
        return FileUtils.expandPath(default)

    return path

def askForUsername():
    return raw_input("Please enter your User-Id: ")

def askForRSAKey():
    return raw_input("Please enter the path to the RSA-Key: ")       

def showMessage(message, newline=True):
    if newline:
        print message
    else:
        sys.stdout.write(message)
        sys.stdout.flush()
