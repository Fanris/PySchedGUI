# -*- coding: utf-8 -*-
'''
Created on 2013-05-23 13:19
@summary: ASCII Tables
@author: predki
'''
def createAsciiTable(*rows):
    '''
    @summary: Creates an ASCII table for output
    @param *rows: Rows to be printed. A Row is a list of Strings
    where each String is the content of one Column. First Row is used as Header
    @result: A String containing the table
    '''
    columnCount = len(rows[0])
    columnLength = {}
    table = []

    # determine Column max width
    for row in rows:
        i = 0
        for word in row:
            #Logger.Log("createAsciiTable", "word: {}".format(word))
            if not word:
                word = ""

            length = len(word)
            key = str(i)
            currentLength = columnLength.get(key, None)

            if not currentLength or currentLength < length:
                columnLength[key] = length
            i = i + 1

    # create table Header
    header = ""
    for i in range(0, columnCount):
        key = str(i)
        header += "| " + rows[0][i].center(columnLength[key]) + " "

    header = header.lstrip("|")
    underline = ""
    for char in header:
        if char == "|":
            underline += "+"
        else:
            underline += "-"

    table.append(header)
    table.append(underline)

    # create rows
    for i in range(1, len(rows)):
        line = ""
        for j in range(0, columnCount):
            key = str(j)
            item = rows[i][j]
            if not item:
                item = ""
            line += "| " + item.center(columnLength[key]) + " "

        line = line.lstrip("|")
        table.append(line)

    return table

def showJobTable(pySchedUI, showArchived=False, showAllUser=False, stateList=None):
    jobs = pySchedUI.getJobs(archived=showArchived, adminMode=showAllUser)

    rows = []
    header = ["ID", "Name", "State", "Added", "Started", "Ended", "Workstation", "Log"]
    rows.append(header)

    if jobs:
        for job in jobs:
            if not stateList:
                rows.append([str(job.get("jobId", None)), job.get("jobName", None), job.get("stateId", None), str(job.get("added", None)), \
                    str(job.get("started", None)), str(job.get("finished", None)), str(job.get("workstation", None)), job.get("log", [])[-1]])
            else:
                for state in stateList:
                    if job.get("stateId", None) == state:
                        rows.append([str(job.get("jobId", None)), job.get("jobName", None), job.get("stateId", None), str(job.get("added", None)), \
                            str(job.get("started", None)), str(job.get("finished", None)), str(job.get("workstation", None)), job.get("log", [])[-1]])
    table = createAsciiTable(*rows)

    asciiTable = ""
    for row in table:
        asciiTable += row + '\r\n'

    print
    print asciiTable   

def showWSTable(pySchedUI):
    workstations, server = pySchedUI.getWorkstations()

    rows = []
    header = ["Machine Name", "PySched Version", "Active Jobs", 
        "CPU Count", "CPU Load", "Memory Load", "Disk (Available / Free)", 
        "Programs", "Machine"]
    rows.append(header)

    # Server
    if server:
        rows.append([                
            str(server.get("workstationName", "N/A")),
            str(server.get("version", "N/A")),
            str(server.get("activeJobs", "N/A")),
            str(server.get("cpuCount", "N/A")),
            str(server.get("cpuLoad", "N/A")),
            str(server.get("memoryLoad", "")),
            "{}GB / {}GB ({}%)".format(
                server.get("diskAvailable", 0),
                server.get("diskFree", 0),
                100 - float(server.get("diskLoad", 100))),
            str(server.get("programs", "N/A")),
            str(server.get("machine", "N/A")),
        ])

    for workstation in workstations:
        rows.append([
            str(workstation.get("workstationName", "N/A")),
            str(workstation.get("version", "N/A")),
            str(workstation.get("activeJobs", "N/A")),
            str(workstation.get("cpuCount", "N/A")),
            str(workstation.get("cpuLoad", "N/A")),
            str(workstation.get("memoryLoad", "N/A")),
            "{}GB / {}GB ({}%)".format(
                workstation.get("diskAvailable", 0),
                workstation.get("diskFree", 0),
                100 - float(workstation.get("diskLoad", 100))),
            str(workstation.get("programs", "N/A")),
            str(workstation.get("machine", "N/A")),
        ])

    table = createAsciiTable(*rows)

    asciiTable = ""
    for row in table:
        asciiTable += row + '\r\n'

    print
    print asciiTable 
