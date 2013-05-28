# -*- coding: utf-8 -*-
'''
Created on 2012-12-04 11:40
@summary: Package for File in / output
@author: Martin Predki
'''

import hashlib
import os
import shutil

def createDirectory(path):
    '''
    @summary: Creates an directory at the given path
    @param path: Path to the directory
    '''
    if not os.path.exists(os.path.normpath(path)):
        os.makedirs(os.path.normpath(path))

    return path

def createFile(pathToFile, filedata):
    '''
    @summary: Creates a file with the given data at the directory
    @param pathToFile: path to directory
    @param filename: The name of the File
    @result: Absolute path to the File
    '''
    path = os.path.expanduser(pathToFile)
    path = os.path.normpath(path)
    dirname = os.path.split(path)[0]

    if not os.path.exists(dirname):
        createDirectory(dirname)

    fileHandler = open(path, "w+")
    if filedata:
        fileHandler.write(filedata)
    fileHandler.close()

    return os.path.normpath(path)

def createOrAppendToFile(pathToFile, filedata):
    '''
    @summary: Creates a file with the given data at the directory
    @param pathToFile: path to directory
    @param filename: The name of the File
    @result: Absolute path to the File
    '''
    path = os.path.expanduser(pathToFile)

    if not os.path.exists(path):
        createFile(path, None)

    with open(os.path.normpath(path), "a") as fileHandler:
        if filedata:
            fileHandler.write(filedata)    

    return os.path.normpath(path)

def deleteFile(pathToFile):
    '''
    @summary: Deletes a file
    @param pathToFile: The file to delete
    @result:
    '''
    path = os.path.expanduser(pathToFile)
    try:
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
    except:
        pass

def clearDirectory(pathToDir, deleteSubfolders=True):
    '''
    @summary: Deletes all files within the folder
    @param pathToDir: path to the folder
    @result:
    '''
    if os.path.isdir(pathToDir):
        files = os.listdir(pathToDir)
        for f in files:
            filepath = os.path.join(pathToDir, f)
            if deleteSubfolders or not os.path.isdir(filepath):
                deleteFile(filepath)

def copyFile(source, dest):
    '''
    @summary: Copies a file from from source to dest
    @param source: File to copy
    @param dest: Destination
    @result:
    '''
    shutil.copy(source, dest)

def moveFile(source, dest):
    '''
    @summary: Copies a file from from source to dest
    @param source: File to copy
    @param dest: Destination
    @result:
    '''
    shutil.move(source, dest)

def validateFileMD5(pathToFile, originalMD5):
    '''
    @summary: Checks the MD5-Hashsum an file against it's original hash
    @param pathToFile: File to check
    @param originalMD5: Original MD5-Hashsum
    @result: True if both Hashsums are equal
    '''
    if getFileMD5Hashsum(pathToFile) == originalMD5:
        return True

    return False

def getFileMD5Hashsum(pathToFile):
    '''
    @summary: Computes the MD5-Hashsum of the given File
    @param pathToFile: Path to file
    @result: The MD5-Hashsum as String
    '''
    md5_hash = hashlib.md5()
    for bytes in readBytesFromFile(pathToFile):
        md5_hash.update(bytes)

    return md5_hash.hexdigest()

def readBytesFromFile(pathToFile, chunk_size=1000):
    '''
    @summary: Reads the given File chunk-wise.
    @param pathToFile: Path to File
    @param chunk_size: Size of each chunk
    @result: Returns the next chunk of the File
    '''
    with open(pathToFile, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)

            if chunk:
                yield chunk
            else:
                break

def getFileSize(pathToFile):
    '''
    @summary: Returns the file size in kb or None, if the file
    does not exists
    @param pathToFile: Path to file.
    @result:
    '''

    if os.path.exists(pathToFile):
        return os.path.getsize(pathToFile) / 1024
    else:
        return None

def readFile(pathToFile):
    '''
    @summary: Reads a complete file
    @param pathToFile:
    @result: Returns a list with all lines
    '''
    path = os.path.expanduser(pathToFile)
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.readlines()    

