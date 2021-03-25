
from PyQt5.QtCore          import *
from PyQt5.QtGui           import *
from PyQt5.QtWidgets       import * 
from icons.icons           import SCR_GetIcon
from widgets.widgets       import SCR_WDG_Tab

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_Test_Tab(SCR_WDG_Tab):

	def __init__(self,config):

		self.config = config

		SCR_WDG_Tab.__init__(self,config)