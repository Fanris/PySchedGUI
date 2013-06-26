#!/usr/bin/env python

from setuptools import setup

setup(name='PySchedGUI',
      version='1.0',
      description='PySchedGUI - The user Interface for PySched.',
      author='Martin Predki',
      author_email='martin.predki@rub.de',
      url='https://github.com/Fanris/PySchedGUI',
      license='LGPL',
      packages=[
            'PySchedGUI',
            'PySchedGUI.UI',
            'PySchedGUI.UI.Menus',
            'PySchedGUI.PySchedUI',            
            'PySchedGUI.PySchedUI.Network'],
      install_requires=['paramiko',],
      scripts=['PySchedUI.sh'],
)
