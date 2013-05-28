# -*- coding: utf-8 -*-
'''
Created on 2013-05-27 12:51
@summary: Functions to parse a Template file
@author: predki
'''

import Common

import os

def ParseTemplate(pathToTemplate):
    '''
    @summary: Parses a template and returns a dictionary containing all the specified values
    @param pathToTemplate: The path to the template
    @result: the template as a dictionary
    '''
    if not os.path.exists(pathToTemplate):
        return False

    with open(pathToTemplate) as templateFile:
        template = {}
        currentSection = ""

        for line in templateFile:
            line = line.strip()
            if line.startswith("#") or line == "":
                continue

            if line.startswith("["):
                currentSection = line.strip("[]")
                continue

            if not parse(line, currentSection, template):
                return False

    return template

def parse(line, section, template):
    '''
    @summary: parses a line and adds its values to the template
    @param line: the line to parse
    @param section: the current section
    @param template: the template to store the values in
    @result:
    '''
    if section.upper() == "CONFIG":
        key, value = line.split("=")

        # transform key to equal the datastructure
        splitted = key.split("_")
        newKey = Common.getCamelCase(splitted)

        if not value or value == "":
            value = None            
        else:
            if value.strip().lower() == "true":
                value = True
            elif value.strip().lower() == "false":
                value = False
            else:
                value = Common.parseToNumber(value)

        template[newKey] = value

        return True

    if section.upper() == "PATH":
        paths = template.get("paths", [])
        if len(paths) == 0:
            paths.append(line)
            template["paths"] = paths
            return True

        paths.append(line)
        return True

    if section.upper() == "COMPILER":
        template["compilerStr"] = line
        return True

    if section.upper() == "PROGRAMS":
        programs = template.get("reqPrograms", [])
        if len(programs) == 0:
            programs.append({"programName": line, "programExec": line})
            template["reqPrograms"] = programs
            return True

        programs.append(line)
        return True

    if section.upper() == "EXECUTION":
        template["executeStr"] = line
        return True

    return False
