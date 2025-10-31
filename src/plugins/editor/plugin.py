"""
File contains all UI widgets regarding the Test Case and Keyword editor grid
"""

from PyQt6.QtCore           import *
from PyQt6.QtGui            import *
from PyQt6.QtWidgets        import * 
from widgets.widgets        import SCR_WDG_Widget
from widgets.widgets        import SCR_WDG_Table_Model
from widgets.widgets        import SCR_WDG_Table
from widgets.plugin_manager import SCR_Plugin

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_EditorPlugin(SCR_Plugin):

    def __init__(self,config,logger,preferences):

        SCR_Plugin.__init__(
                                self,
                                name="Editor",
                                author="stefan.dragomir",
                                version="1.0.0",
                                config=config,
                                logger=logger,
                                preferences=preferences)

    def load(self):

        self.draw_gui()

        self.subscribe()

    def unload(self):

        pass

    def draw_gui(self):

        self.table = SCR_WDG_Table(
                                    config=self.config, 
                                    search_clbk=None, 
                                    with_metadata=True, 
                                    model_class=SCR_WDG_EditorGrid_Model)

        pass

    def subscribe(self):

        self.messenger.subscribe("TestTreeSelectionChange", self.on_test_tree_selection_change)

    def on_test_tree_selection_change(self,data):

        print("editor change")
        print(data)


"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_EditorGrid_Model(SCR_WDG_Table_Model):

    def __init__(self,config,parent):

        SCR_WDG_Table_Model.__init__(self,config,parent)

    def load(self,data,parent):

        print("load")