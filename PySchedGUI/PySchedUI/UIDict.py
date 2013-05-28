# -*- coding: utf-8 -*-
'''
Created on 2013-03-25 15:45
@summary: 
@author: Martin Predki
'''

class UIDict(object):
    '''
    @summary: This dictionary holds all UI input infos.
    '''

    def __init__(self):
        self.nameLookup = {}
        self.infos = {}

    def addInfo(self, screenName, attrName, value):
        '''
        @summary: Adds an Information to this data structure
        @param screenName: The name that is shown by validating functions.
        @param valueName: the intern attribute name
        @param value: the attribute value.
        @result: 
        '''
        self.infos[attrName] = value
        self.nameLookup[attrName] = screenName

    def getInfos(self):
        '''
        @summary: returns the JobInformations.
        @result: 
        '''
        return self.infos

    def getScreenName(self, attrName):
        '''
        @summary: Returns the screenName of the attribute
        @param attrName: the attribute
        @result: 
        '''
        return self.nameLookup.get(attrName, "")

    def get(self, attrName, default):
        return self.infos.get(attrName, default)

    def update(self, d):
        self.infos.update(d)
