# -*- coding: utf-8 -*-
'''
Created on 2012-10-08 16:09
@summary: PySched User Script
@author: Martin Predki
'''

from Network import Network
from Common import pack, deleteFile
from UIDict import UIDict

import TemplateParser
import FileUtils

import os
import logging

class PySchedUI(object):
    '''
    @summary: PySchedUI Class
    '''

    def __init__(self, args, cmd=None):
        '''
        @summary: Initializes the PySchedUI
        @result:
        '''
        self.initializeLogger(args)
        self.debug = args.debug
        self.userId = args.user or None        
        self.rsaKey = args.key or None
        self.lastError = None
        self.network = None

        if cmd:
            self.logger.debug("Command = {}".format(cmd))
            if self.openConnection():
                if cmd.lower() == "addjob":
                    uiDict = UIDict()
                    uiDict.addInfo("Template-File", "template", os.path.normpath(args.template))
                    uiDict.addInfo("Username", "userId", self.userId)
                    self.logger.info("Scheduling job from {}".format(args.template))
                    self.addJob(uiDict.getInfos())
                    print
                    print
                self.closeConnection()

    def openConnection(self):
        self.network = Network(self, self.debug, keyFile=self.rsaKey)
        if self.network.openConnection():
            userAuth, self.admin = self._checkUser(self.userId)
            if not userAuth:
                self.lastError = "Unable to log in with this User. Please contact your system administrator."
                self.logger.error(self.lastError)
                return False
            return True

    def closeConnection(self):
        self.logger.info("Closing connection...")
        if self.network:
            self.network.closeConnection()            

    def saveRSA(self, rsa):
        FileUtils.createFile("~/.pyschedGUI", rsa)

    def loadRSA(self):
        rsa = FileUtils.readFile("~/pyschedGUI")
        if rsa and len(rsa) > 0:
            return FileUtils.readFile("~/.pyschedGUI")[0]
        else:
            return None

    def initializeLogger(self, args):
        '''
        @summary: Initializes the logger
        @param workingDir:
        @param args:
        @result:
        '''
        self.logger = logging.getLogger("PySchedUI")
        self.logger.setLevel(logging.DEBUG)

        # create console handler and set level
        ch = logging.StreamHandler()
        if args.quiet:
            ch.setLevel(logging.ERROR)
        elif args.debug:
            ch.setLevel(logging.DEBUG)
        else:
            ch.setLevel(logging.INFO)

        # create formatter
        formatter = logging.Formatter('[%(levelname)s]: %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(ch)


# =================== COMMANDS ====================================

    def addJobs(self, listOfJobConfigs):
        for job in listOfJobConfigs:
            uiDict = {}
            uiDict["template"] = job
            self._addJob(uiDict)

    def _addJob(self, uiDict):
        '''
        @summary: Adds a job with a template
        @param userId: the userId
        @param template: the path to the template or a template
        @result:
        '''
        uiDict["userId"] = self.userId
        if uiDict.get("template", None):
            uiDict.update(TemplateParser.ParseTemplate(uiDict.get("template", None)))
            del uiDict["template"]

        paths = uiDict.get("paths", [])
        if "paths" in uiDict:
            del uiDict["paths"]

        self.logger.debug(paths)

        returnValue = self.network.sendCommand("addJob", **uiDict)

        if returnValue.get("result", False):
            jobId = returnValue.get("jobId", None)

            if not jobId:
                return False

            path = pack("{}.tar".format(jobId), *paths)
            self.logger.info("Sending Files... ")
            if path:                
                self.logger.debug("Sending File... {} ".format(path))
                returnValue = self.network.sendFile(path)
                deleteFile(path)

                if returnValue.get("result", False):
                    return True
                    self.logger.info("Done")
                else:
                    return False

            return True
        else:
            return False

    def _checkUser(self, userId):
        returnValue = self.network.sendCommand("checkUser", waitForResponse=True, userId=userId )
        return returnValue.get("result", False), returnValue.get("admin", False)

    def createUser(self, email, firstName="", lastName="", isAdmin=False):
        param = {
            "userId": self.userId,
            "email": email,
            "firstName": firstName,
            "lastName": lastName,
            "admin": isAdmin
        }
        return self._createUser(param)

    def _createUser(self, uiDict):
        returnValue = self.network.sendCommand("createUser", **uiDict)
        if not returnValue.get("result", False):
            self.lastError = "Could not create User"
            return False
        else:
            return True

    def getJobs(self, archived=False, adminMode=False):
        param = {
            "userId": self.userId,
            "showAll": archived,
            "showAllUser": adminMode and self.admin
        }
        return self._getJobs(param)

    def _getJobs(self, uiDict):
        returnValue = self.network.sendCommand("getJobs", **uiDict)
        return returnValue.get("jobs", None)

    def getWorkstations(self):
        return self._getWorkstations()

    def _getWorkstations(self):
        returnValue = self.network.sendCommand("getWorkstations", userId=self.userId)
        return returnValue.get("workstations", []), returnValue.get("server", None)

    def getJobLog(self, jobId):
        param = {
            "userId":   self.userId,
            "jobId":    jobId,
        }
        self._getJobLog(param)

    def _getJobLog(self, uiDict):
        returnValue = self.network.sendCommand("getJobLog", waitForResponse=True, **uiDict)
        return returnValue.get("log", None)

    def getCompiler(self):
        return self.network.sendCommand("getCompiler").get("compiler", None)

    def abortJobs(self, jobIdList):
        for jobId in jobIdList:
            param = {
                "userId":   self.userId,
                "jobId":    self.jobId,
            }
            self._abortJob(param)

    def _abortJob(self, uiDict):
        returnValue = self.network.sendCommand("killJob", **uiDict)
        if returnValue.get("result", False):
            return False

        return True

    def checkJobs(self):
        self.network.sendCommand("checkJobs", waitForResponse=False)

    def archiveJob(self, jobId, userId):
        self.network.sendCommand("archiveJob", waitForResponse=False, userId=userId, jobId=jobId)

    def forceSchedule(self):
        self.network.sendCommand("schedule", waitForResponse=False)

    def pauseJobs(self, jobIdList):
        for jobId in jobIdList:
            param = {
                "userId":   self.userId,
                "jobId":    jobId,
            }
            self._pauseJob(param)
        return True

    def _pauseJob(self, uiDict):
        self.network.sendCommand("pauseJob", waitForResponse=False, **uiDict)

    def resumeJobs(self, jobIdList):
        for jobId in jobIdList:
            param = {
                "userId":   self.userId,
                "jobId":    jobId,
            }
            self._resumeJob(param)
        return True

    def _resumeJob(self, uiDict):
        self.network.sendCommand("resumeJob", waitForResponse=False, **uiDict)        

    def getResults(self, jobIdList, path):
        for jobId in jobIdList:
            param = {
                "userId"    : self.userId,
                "jobId"     : jobId,
                "path"      : path,
            }
            self._getResults(param)

    def _getResults(self, uiDict):
        returnValue = self.network.sendCommand("getResults", **uiDict)
        
        return self.network.getFile(
            os.path.join(
                uiDict.get("path", ""), 
                returnValue.get("filename", "results.tar")))

    def deleteJobs(self, jobIdList):
        for jobId in jobIdList:
            param = {
                "userId"    : self.userId,
                "jobId"     : jobId,
            }
            self._deleteJob(param)        

    def _deleteJob(self, uiDict):
        returnValue = self.network.sendCommand("deleteJob", waitForResponse=True, **uiDict)
        if returnValue.get("result", False):
            return True
        return False

    def shutdownServer(self, uiDict):
        self.network.sendCommand("shutdown", waitForResponse=True, **uiDict)