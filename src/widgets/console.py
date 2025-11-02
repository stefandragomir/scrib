"""
File contains all UI widgets regarding the Scrib UI Debug Console
"""

from PyQt6.QtCore          import *
from PyQt6.QtGui           import *
from PyQt6.QtWidgets       import * 
from widgets.widgets       import SCR_WDG_Widget
from widgets.widgets       import SCR_WDG_PlainTextEdit

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_Console(SCR_WDG_Widget):

    def __init__(self,config):

        SCR_WDG_Widget.__init__(self,config)

        self.config = config

        self.entries = 0

        self.max_entries = 500

        self.draw_gui()

    def draw_gui(self):

        self.ly = QVBoxLayout()

        self.text_area = SCR_WDG_PlainTextEdit(self.config)

        self.ly.addWidget(self.text_area) 

        self.setLayout(self.ly)

        self.text_area.setReadOnly(True)

        _css = ""
        _css += "border: 1px solid {};".format(self.config.get_theme_color_border())

        self.setStyleSheet(_css)

        _font = QFont("Consolas", 10)
        _font.setFixedPitch(True)

        self.text_area.setFont(_font)

    def write(self,text):

        if self.entries > self.max_entries:

            self.entries = 0

            self.text_area.clear()

        self.entries += 1

        self.text_area.appendPlainText(text)