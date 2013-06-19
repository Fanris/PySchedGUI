# -*- coding: utf-8 -*-
'''
Created on 2013-05-23 13:23
@summary: Add Job Menu
@author: predki
'''

from IMenu import IMenu
from PySchedGUI.PySchedUI.UIDict import UIDict

import CommonUI
import Tables

import os


class AddJobMenu(IMenu):
    def __init__(self, pySchedUI):
        super(AddJobMenu, self).__init__(pySchedUI)

    def show(self):
        '''
        @summary: Shows the add Job dialog with template supoort
        @result:
        '''
        inp = UIDict()
        print
        print "Adding a new job..."
        print "================================================"
        inp.addInfo("Jobname", "jobName", 
            CommonUI.getTextInput("Please enter a job name"))

        inp.addInfo("Description", "jobDescription", 
            CommonUI.getTextInput("(Optional) A short description of the job"))

        print "Please enter the path to the PySched-Config file or nothing if you want to create a new template:"
        temp = CommonUI.getPathInput("")
        if temp != "":
            inp.addInfo("Template-File", "template", os.path.normpath(temp))
        else: 
            inp = self.createTemplate(inp)

        if CommonUI.showValidatingInput(inp):
            if self.pySchedUI.addJob(inp.getInfos()):
                Tables.showJobTable(self.pySchedUI)

    def createTemplate(self, inp):
            '''
            @summary: Creates a new Template File.
            @param inp: input parameter.
            @result: 
            '''
            newInp = UIDict()
            newInp.addInfo("Username", "userId", inp.get("userId", ""))
            newInp.addInfo("Job Name", "jobName", inp.get("jobName", ""))
            newInp.addInfo("Job Description", "jobDescription", inp.get("jobDescription", ""))
            
            print
            print "Which operating system is needed for the job (default: Linux, '?' for help)?."

            selected = CommonUI.getTextInput("", "Linux", help=REQ_OS_HELP) 

            newInp.addInfo("Required OS", "reqOS", selected)

            print
            print "Is the Job capable of using multiple CPU-Cores? (y/n):"
            newInp.addInfo("Multiple CPU's", "multiCpu", CommonUI.showYesNo("> "))

            print
            print "How many CPU-Cores must be available for the Job (default: 1)?"
            selected = CommonUI.getIntInput("", 1, help=REQ_CPU_HELP)            
            newInp.addInfo("Required CPU-Cores", "minCpu", selected)

            print
            print "Please specify which files should be transferred to the server."            
            print "Nothing to move on, '?' for help"
            paths = []
            tmp = CommonUI.getPathInput("", "", help=PATH_HELP)
            while tmp != "":
                paths.append(tmp)
                newInp.addInfo("Copy Paths", "paths", paths)
                tmp = CommonUI.getTextInput("", "", help=PATH_HELP)

            print
            print "If the job needs to be compiled, please enter the compile string ('?' for help)."
            selected = CommonUI.getTextInput("", help=COMPILER_HELP)
            if not selected == "":
                newInp.addInfo("Compiler String", "compilerStr", selected)

            print
            print "Please specify any special program, that your job needs."
            print "Leave blank if no program is needed, '?' for help."
            programs = []
            tmp = CommonUI.getTextInput("", "", help=PROGRAMS_HELP)
            while tmp != "":
                programs.append(tmp)
                newInp.addInfo("Required Programs", "reqPrograms", programs)
                tmp = CommonUI.getTextInput("", "", help=PROGRAMS_HELP)          

            print
            print "Please enter the execution string."            
            selected =  CommonUI.getTextInput("", "", help=EXECUTION_HELP)
            if not selected == "":
                newInp.addInfo("Execute String", "executeStr", selected)

            return newInp

REQ_OS_HELP = """
Changes to this variable may result in not scheduling your
job if the given OS is not available within the network.
For further informations please contact your administrator."""

REQ_CPU_HELP =  """
Sets the CPU count that should be at least reserved for the
program. Setting this to a high value may result in a longer
scheduling time till a workstation that matches the
requirement is free. This option is only used by the parser
if MULTI_CPU is true."""

PATH_HELP = """
This section defines the files that are needed by the program.
All files specified here are send to the server. If a folder is
specified the content will be send to the server.

Examples:
/home/user/HelloWorld.c will send the file HelloWorld.c to the server
/home/user/foo/ will send the complete folder to the server
/home/user/foo/* will send the content of the folder foo to the server"""

COMPILER_HELP = """
This section is only needed if the program needs to be
compiled first. The compilation will be done on the server.
Please make sure that the needed compiler and all libraries
are installed on the server or provided via the PATH section.
If you are using a linux OS it may be simpler to compile the
code on your machine and link (static linking) all necessary
files with the executable.

Example: If you have specified the file HelloWorld.c at the
PATH section and want to compile this file with the
gcc-compiler (installed on the server) the compiler code
should look like:
gcc -o helloWorld HelloWorld.c"""

PROGRAMS_HELP = """
This section is only needed if the program (or - more likely
- the script) needs a special environment (in this case a
special program) to run. Here you can provide a list of
programs which must be available on the workstation. To use
this feature it is highly recommended to speak with your
administrator first because the specified program may not be
listed within the scheduler and thus your program will never
be started. In fact it is possible to provide any program
(make sure you provide the name of the executable) and the
scheduler will ask the workstations for this program but this
is not recommended."""

EXECUTION_HELP = """
This section describes how the program should be started on
the workstation. Here you must provide a bash command like
if you would start the program on your own machine.

Example:
To start the compiled HelloWorld program simply enter:
helloWorld"""
        
