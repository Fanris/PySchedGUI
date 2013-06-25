# -*- coding: utf-8 -*-
'''
Created on 2012-10-08 16:09
@summary: PySched User Script
@author: Martin Predki
'''

from Network import Network
from Common import pack
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
        self.version = "1.1.0"

        self.initializeLogger(args)
        self.debug = args.debug
        self.userId = args.user or None        
        self.rsaKey = args.key or None
        self.lastError = None
        self.network = None
        self.isAdmin = False
        self.multicastGroup = args.multicast
        self.server = args.server or None

        if cmd:
            self.logger.debug("Command = {}".format(cmd))
            if self.openConnection():
                if cmd.lower() == "addjob":
                    uiDict = UIDict()
                    uiDict.addInfo("Template-File", "template", os.path.normpath(FileUtils.expandPath(args.template)))
                    uiDict.addInfo("Username", "userId", self.userId)
                    self.logger.info("Scheduling job from {}".format(args.template))
                    self.addJob(uiDict.getInfos())
                    print
                    print
                self.closeConnection()

    def openConnection(self):
        self.network = Network(
            self, 
            self.debug, 
            keyFile=FileUtils.expandPath(self.rsaKey), 
            multicast=self.multicastGroup,
            server=self.server)

        if self.network.openConnection():
            userAuth, self.isAdmin = self._checkUser(self.userId)
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
        rsa = FileUtils.readFile("~/.pyschedGUI")
        if rsa and len(rsa) > 0:
            return rsa[0]
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

    def addJobConfigFile(self, configFile):
        uiDict = {}
        uiDict["template"] = configFile
        return self._addJob(uiDict)        

    def addJob(self, jobInfo):
        return self._addJob(jobInfo)

    def _addJob(self, uiDict):
        '''
        @summary: Adds a job with a template
        @param userId: the userId
        @param template: the path to the template or a template
        @result:
        '''
        uiDict["userId"] = self.userId
        if uiDict.get("template", None):
            jobDict = TemplateParser.ParseTemplate(uiDict.get("template", None))
            uiDict.update(jobDict)
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

            returnValue = self.network.sendCommand("requestFileUpload", jobId=jobId)
            if not returnValue:
                return

            remotePath = returnValue.get("path", None)

            if remotePath:
                try:
                    path = pack("{}.tar".format(jobId), *paths)
                    if path:                
                        self.network.sendFileSFTP(path, remotePath, callback=None)                    
                        FileUtils.deleteFile(path)
                        self.network.sendCommand("fileUploadCompleted", waitForResponse=True, path=remotePath, jobId=jobId)
                        return True
                    else:
                        self.deleteJobs([jobId])
                        return False
                except:
                    self.deleteJobs([jobId])
                    #self.lastError = e
            
        return False

    def _checkUser(self, userId):
        returnValue = self.network.sendCommand("checkUser", waitForResponse=True, userId=userId )
        return returnValue.get("result", False), returnValue.get("admin", False)

    def createUser(self, user):
        param = {
            "userId": self.userId,
            "email": user.email,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "admin": user.admin
        }
        return self._createUser(param)

    def _createUser(self, uiDict):
        returnValue = self.network.sendCommand("createUser", **uiDict)
        if not returnValue.get("result", False):
            self.lastError = "Could not create User"
            return False
        else:
            return True

    def getUsers(self):
        param = {
            "userId": self.userId
        }
        return self._getUsers(param)

    def _getUsers(self, uiDict):
        returnValue = self.network.sendCommand("getUsers", **uiDict)
        if returnValue and returnValue.get("result", False):
            return returnValue.get("users", None)

    def deleteUser(self, email):
        param = {
            "userId": self.userId,
            "email": email
        }
        return self._deleteUser(param)

    def _deleteUser(self, uiDict):
        returnValue = self.network.sendCommand("deleteUser", **uiDict)
        if returnValue:
            return returnValue.get("result", False)

    def getJobs(self, archived=False, adminMode=False):
        param = {
            "userId": self.userId,
            "showAll": archived,
            "showAllUser": adminMode and self.isAdmin
        }
        return self._getJobs(param)

    def _getJobs(self, uiDict):
        returnValue = self.network.sendCommand("getJobs", **uiDict)
        if returnValue:
            return returnValue.get("jobs", None)

    def getWorkstations(self):
        return self._getWorkstations()

    def _getWorkstations(self):
        returnValue = self.network.sendCommand("getWorkstations", userId=self.userId)
        if returnValue:
            return returnValue.get("workstations", []), returnValue.get("server", None)

    def getJobLog(self, jobId):
        param = {
            "userId":   self.userId,
            "jobId":    jobId,
        }
        return self._getJobLog(param)

    def _getJobLog(self, uiDict):
        returnValue = self.network.sendCommand("getJobLog", waitForResponse=True, **uiDict)
        if returnValue:
            return returnValue.get("log", "")

    def abortJobs(self, jobIdList):
        for jobId in jobIdList:
            param = {
                "userId":   self.userId,
                "jobId":    jobId,
            }
            self._abortJob(param)

    def _abortJob(self, uiDict):
        returnValue = self.network.sendCommand("killJob", **uiDict)
        if returnValue and returnValue.get("result", False):
            return True

        return False

    def addProgram(self, program):
        param = {
            "userId": self.userId,
            "programName": program.programName,
            "programPath": program.programPath,
            "programExec": program.programExec,
            "programVersion": program.programVersion,
        }
        return self._addProgram(param)

    def _addProgram(self, uiDict):
        returnValue = self.network.sendCommand("addProgram", **uiDict)
        if returnValue:
            return returnValue.get("result", False)

    def getPrograms(self):
        return self._getPrograms()

    def _getPrograms(self):
        returnValue = self.network.sendCommand("getPrograms")
        if returnValue:
            return returnValue.get("programs", None)

    def deleteProgram(self, programName):
        param = {
            "userId": self.userId,
            "programName": programName
        }
        return self._deleteProgram(param)

    def _deleteProgram(self, uiDict):
        returnValue = self.network.sendCommand("deleteProgram", **uiDict)
        if returnValue:
            return returnValue.get("result", False)

    def checkJobs(self):
        self.network.sendCommand("checkJobs", waitForResponse=False, userId=self.userId)

    def archiveJob(self, jobId, userId):
        self.network.sendCommand("archiveJob", waitForResponse=False, userId=userId, jobId=jobId)

    def forceSchedule(self):
        param = {
            "userId": self.userId,
        }
        self.network.sendCommand("schedule", waitForResponse=False, **param)

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

    def updateJobData(self, jobId, fileList):
        param = {
            "jobId": jobId,
            "paths": fileList,
            "userId": self.userId
        }
        return self._updateJobData(param)

    def _updateJobData(self, uiDict):
        paths = uiDict.get("paths", [])
        jobId = uiDict.get("jobId", None)
        
        path = pack("{}.tar".format(jobId), *paths)
        if path:                
            self.logger.debug("Sending File... {} ".format(path))
            returnValue = self.network.sendCommand("requestFileUpload", jobId=jobId)
            if not returnValue:
                return

            remotePath = returnValue.get("path", None)

            if remotePath:
                path = pack("{}.tar".format(jobId), *paths)
                self.logger.info("Sending Files... ")
                if path:                
                    self.network.sendFileSFTP(path, remotePath, callback=None)                    
                    FileUtils.deleteFile(path)
                    self.network.sendCommand("fileUploadCompleted", waitForResponse=True, path=remotePath, jobId=jobId)
                    return True
        else:
            return False

        return False

    def getResultsByJobId(self, jobIdList, path):
        for jobId in jobIdList:
            param = {
                "userId"    : self.userId,
                "jobId"     : jobId,
                "path"      : path,
            }
            self.logger.info("Get Results of {}".format(jobId))
            self._getResultsSFTP(param)
        return True

    def getAllResults(self, path):
        jobs = self.getJobs()
        endStates = [
             "DONE",
             "ABORTED",
             "SCHEDULER_ERROR",
             "COMPILER_ERROR",
             "WORKSTATION_ERROR",
             "PERMISSION_DENIED",
             "ERROR",
        ]
        for job in jobs:
            if job.get("stateId", None) in endStates:
                param = {
                    "userId"    : self.userId,
                    "jobId"     : job.get("jobId", ""),
                    "path"      : path,
                }
                self._getResultsSFTP(param)
        return True

    def _getResultsSFTP(self, uiDict):
        jobId = uiDict.get("jobId", None)
        returnValue = self.network.sendCommand("requestFileDownload", **uiDict)
        if returnValue and returnValue.get("result", False):
            localPath = uiDict.get("path", None)
            remotePath = returnValue.get("path", None)
            if remotePath and localPath:
                filename = os.path.split(remotePath)[1]
                localPath = os.path.join(localPath, filename)
                self.network.getFileSFTP(localPath, remotePath, callback=None)
                self.network.sendCommand("fileDownloadCompleted", waitForResponse=True,
                    path=remotePath, jobId=jobId)

    def deleteJobs(self, jobIdList):
        for jobId in jobIdList:
            param = {
                "userId"    : self.userId,
                "jobId"     : jobId,
            }
            self._deleteJob(param)        
        return True

    def _deleteJob(self, uiDict):
        returnValue = self.network.sendCommand("deleteJob", waitForResponse=True, **uiDict)
        if returnValue and returnValue.get("result", False):
            return True
        return False

    def shutdownServer(self):
        self.network.sendCommand("shutdown", waitForResponse=False, userId=self.userId)
        return True

    def shutdownAll(self):
        self.network.sendCommand("shutdownAll", waitForResponse=False, userId=self.userId)
        return True

    def shutdownWs(self, listOfWorkstationNames):
        for ws in listOfWorkstationNames:
            self.network.sendCommand("shutdownWorkstation", 
                waitForResponse=True, 
                userId=self.userId,
                workstationName=ws)
        return True

    def setMaintenanceMode(self, listOfDicts):
        '''
        @summary: Set Maintenance Mode for the given workstations.
        @param listOfDicts: key = WorkstationName, Value = True or False wether 
        the workstation should set to maintenance or not
        @result: 
        '''
        for d in listOfDicts:
            d["userId"] = self.userId
            self._setMaintenance(d)
        return True

    def _setMaintenance(self, uiDict):
        self.network.sendCommand("setMaintenance", **uiDict)


    def fileDownloadCompleted(self, pathToFile, jobId):
        self.network.sendCommand("fileDownloadCompleted", waitForResponse=False,
            path=pathToFile, jobId=jobId)
        return True

    def getJobFolder(self, jobId):
        param = {
            "userId": self.userId,
            "jobId": jobId
        }
        return self._getJobFolder(param)

    def _getJobFolder(self, uiDict):
        returnValue = self.network.sendCommand("getJobDirStruct", **uiDict)
        if returnValue:
            return returnValue.get("content", [])

    def getFileContent(self, jobId, path, lineCount=0):
        param = {
            "userId": self.userId,
            "jobId": jobId,       
            "path": path,
            "lineCount": lineCount, 
        }
        return self._getFileContent(param)

    def _getFileContent(self, uiDict):
        returnValue = self.network.sendCommand("getFileFromWS", **uiDict)
        if returnValue:
            return returnValue.get("content", [])

    def updateWorkstations(self, workstations):
        for workstationName in workstations:
            if "server" in workstationName.lower():
                workstationName = None
                
            param = {
                "userId": self.userId,
                "workstationName": workstationName
            }
            return self._updateWorkstation(param)

    def _updateWorkstation(self, uiDict):
        returnValue = self.network.sendCommand("updatePySched", **uiDict)
        if returnValue:
            return returnValue.get("result", False)

    def updateSchedulingParams(self, params):
        returnValue = self.network.sendCommand("updateSchedulingParams",
            params=params,
            userId=self.userId)
        if returnValue:
            return returnValue.get("result", False)

    def getSchedulingParams(self):
        returnValue = self.network.sendCommand("getSchedulingParams", userId=self.userId)
        if returnValue and returnValue.get("result", False):
            return returnValue.get("params", {})
