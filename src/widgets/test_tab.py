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

	def __init__(self,config,plugins):

		self.config  = config
		self.plugins = plugins

		SCR_WDG_Tab.__init__(self,config)

		self.draw_gui()

	def draw_gui(self):

		for _plugin in self.plugins:

			self.draw_plugin(_plugin)

	def draw_plugin(self,plugin):

		_wdg_tab = self.add_tab(plugin.instance.name)

		plugin.instance.load()

		self.ly = QVBoxLayout()

		self.ly.addWidget(plugin.instance)

		_wdg_tab.setLayout(self.ly)
