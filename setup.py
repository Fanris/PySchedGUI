#!/usr/bin/env python

from setuptools import setup

setup(name='PySchedGUI',
      version='1.1',
      description='PySchedGUI - A graphical user Interface for PySched.',
      author='Martin Predki',
      author_email='martin.predki@rub.de',
      url='https://github.com/Fanris/PySchedGUI',
      license='LGPL',
      packages=[
            'PySchedGUI',
            'PySchedGUI.GUI',
            'PySchedUI',            
            'PySchedUI.Network'],
      install_requires=['paramiko',],
      scripts=['PySchedGUI/PySchedGUI.sh'],
)
