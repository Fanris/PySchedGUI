# -*- coding: utf-8 -*-
'''
Created on 2013-05-23 13:21
@summary: Standard Menu Interface
@author: predki
'''

class IMenu(object):
	def __init__(self, pySchedUI):
		self.pySchedUI = pySchedUI

	def show(self):
		raise NotImplementedError
