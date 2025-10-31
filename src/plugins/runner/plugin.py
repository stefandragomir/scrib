"""
File contains all UI widgets regarding the Test Case execution
"""

from PyQt6.QtCore           import *
from PyQt6.QtGui            import *
from PyQt6.QtWidgets        import * 
from widgets.widgets        import SCR_WDG_Widget
from widgets.plugin_manager import SCR_Plugin

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_EditorPlugin(SCR_Plugin):

    def __init__(self,config,logger,preferences):

        SCR_Plugin.__init__(
                                self,
                                name="Runner",
                                author="stefan.dragomir",
                                version="1.0.0",
                                config=config,
                                logger=logger,
                                preferences=preferences)

    def load(self):

        self.draw_gui()

    def unload(self):

        pass

    def draw_gui(self):

        pass
