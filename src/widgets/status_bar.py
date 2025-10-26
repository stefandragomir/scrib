"""
File contains all UI widgets regarding the Status Bar
"""

from PyQt6.QtCore          import *
from PyQt6.QtGui           import *
from PyQt6.QtWidgets       import * 
from icons.icons           import SCR_GetIcon
from widgets.widgets       import SCR_WDG_StatusBar
from widgets.widgets       import SCR_WDG_Label
from widgets.widgets       import SCR_WDG_ActionBar


"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_MainStatusBar(SCR_WDG_StatusBar):

    def __init__(self,app,config):

        SCR_WDG_StatusBar.__init__(self,config)

        self.app = app

        self.draw_gui()

    def draw_gui(self):

        self.wdg_lbl    = SCR_WDG_Label(self.config)
        self.wdg_action = SCR_WDG_ActionBar(
        										self.app,
        										self,
        										self.config)

        self.addPermanentWidget(self.wdg_action)   
        self.addPermanentWidget(self.wdg_lbl) 	

    def label(self,text):

        self.wdg_lbl.setText(text)

    def message(self,text):

    	self.wdg_action.message(text)

    def start(self,withload=False,withcancel=False):

    	self.wdg_action.start(withload,withcancel)

    def stop(self):

    	self.wdg_action.stop()

    def progress(self,value):

    	self.wdg_action.progress(value)
