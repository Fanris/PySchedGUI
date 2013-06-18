import os
import tarfile


def getCamelCase(s):
    tl = [s[0].lower()]
    for t in s[1::]:
        if t in ['OS']:
            tl.append(t)
        else:
            tl.append(t.title())
    return ''.join(tl)

def parseToNumber(s):
    if not s:
        return None

    try:
        n = int(s)
        return n
    except ValueError:
        return s

def pack(outputPath, *args):
    '''
    @summary: Creates an uncompressed tar-File with all files specified in args.
    @param outputPath: Output Path for the TAR-Archiv
    @param firstFolderContentInRoot: A flag specifying if the content of folders given in args should
    be stored at the root folder of the archive. So the parent directory of the given folder is splitted.
    E.g. args = /foo/bar.txt is packed as bar.txt in the archive.
    @param *args: List of files to put into the archive
    @result:
    '''
    if len(args) == 0:
        return None

    tar = tarfile.open(outputPath, "w")
    for filename in args:
        filename = filename.strip()
        if not os.path.exists(filename.strip("*")):
            print "Error on creating archive! File {} does not exist!".format(filename.strip("*"))
            return False

        if filename.endswith("*"):
            filename = filename.strip("*")
            if os.path.isdir(filename):
                files = os.listdir(filename)
                for secFilename in files:
                    arcName = secFilename
                    addToArchive(tar, os.path.join(filename, secFilename), arcName)
        else:
            arcName = os.path.split(filename)[1]
            addToArchive(tar, filename, arcName)

    tar.close()
    return outputPath

def addToArchive(tar, filename, arcName):
    '''
    @summary: Recursive function.
    Adds a file or directory to an tar archive
    @param tar: an tar object to add the file to
    @param filename: the filename
    @param arcName: the filename within the archive
    '''
    #print "packing {}".format(filename)
    if os.path.isdir(filename):
        files = os.listdir(filename)
        for f in files:
            f = f.strip()
            addToArchive(tar, os.path.join(filename, f), os.path.join(arcName, os.path.split(f)[1]))

    else:
        tar.add(name=filename, arcname=arcName)
