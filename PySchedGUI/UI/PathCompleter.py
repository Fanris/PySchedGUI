# -*- coding: utf-8 -*-
'''
Created on 2013-04-22 14:54
@summary: 
@author: Martin predki
'''

from PySchedGUI.PySchedUI import FileUtils

import os
import readline
import atexit

class PathCompleter(object):    
    '''
    @summary: Implements history path auto completion for all user input
    '''
    def __init__(self):
        history_file = os.path.expanduser('~/.PySchedUI_history')
        atexit.register(readline.write_history_file, history_file)

    def _listdir(self, root):
        "List directory 'root' appending the path separator to subdirs."
        res = []
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                name += os.sep
            res.append(name)
        return res

    def complete(self, text, state):
        line = readline.get_line_buffer().split()        
        "Perform completion of filesystem path."
        dirname, rest = os.path.split(line[0])
        dirname = FileUtils.expandPath(dirname)
        rest = FileUtils.expandPath(rest)
        if dirname == '':
            dirname = '/'

        if rest == '':
            name = self._listdir(dirname)
            return name[state]

        else:
            tmp = self._listdir(dirname)
            name = []
            for t in tmp:
                if t.startswith(rest):
                    name.append(t)
            return name[state]
