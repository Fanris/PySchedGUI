# -*- coding: utf-8 -*-
'''
Created on 2013-05-23 13:33
@summary: Create / Edit User UI
@author: predki
'''

from IMenu import IMenu

from PySchedUI.UIDict import UIDict
from PySchedUI.DataStructures import User

import CommonUI

class UserMenu(IMenu):
    def __init__(self, pySchedUI):
        super(UserMenu, self).__init__(pySchedUI)

    def show(self):
        '''
        @summary: Shows the create new user dialog.
        @param args:
        @result:
        '''
        inp = UIDict()
        print
        print "Creating an new User..."
        print "================================================"
        inp.addInfo("Email", "email", raw_input("Please enter the email address: "))
        inp.addInfo("First Name", "firstName", raw_input("Please enter the first name (Optional): "))
        inp.addInfo("Last Name", "lastName", raw_input("Please enter the last name (Optional): "))
        inp.addInfo("Administrator", "admin", CommonUI.showYesNo("New user is an administrator (y/n): "))

        if CommonUI.showValidatingInput(inp):
            u = User()
            u.email = inp.get("email", "")
            u.firstName = inp.get("firstName", "")
            u.lastName = inp.get("lastName", "")
            u.admin = inp.get("admin", False)
            if self.pySchedUI.createUser(u):
                print "User {} created.".format(inp.get("email", None))
            else:
                print "Failed to create user."
