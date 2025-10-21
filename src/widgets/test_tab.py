"""
File contains all UI widgets regarding the Central Test Tab
"""

from PyQt6.QtCore          import *
from PyQt6.QtGui           import *
from PyQt6.QtWidgets       import * 
from icons.icons           import SCR_GetIcon
from widgets.widgets       import SCR_WDG_Tab

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_Test_Tab(SCR_WDG_Tab):

	def __init__(self,config):

		self.config = config

		SCR_WDG_Tab.__init__(self,config)