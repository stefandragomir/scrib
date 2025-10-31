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

		self.draw_gui()

	def draw_gui(self):

		pass

		# self.wdg_editor      = self.add_tab("Edit")
		# self.wdg_editor_grid = SCR_WDG_EditorGrid(self.config,self.wdg_editor)

		# self.ly = QVBoxLayout()

		# self.ly.addWidget(self.wdg_editor_grid)

		# self.wdg_editor.setLayout(self.ly)

		# #debug
		# self.wdg_editor_grid.populate()