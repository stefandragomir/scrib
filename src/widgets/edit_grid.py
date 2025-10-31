"""
File contains all UI widgets regarding the Test Case and Keyword editor grid
"""

from PyQt6.QtCore          import *
from PyQt6.QtGui           import *
from PyQt6.QtWidgets       import * 
from widgets.widgets       import SCR_WDG_Widget
from widgets.widgets       import SCR_WDG_Table_Model
from widgets.widgets       import SCR_WDG_Table
from messenger.messenger   import SCR_Messenger

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_EditorGrid(SCR_WDG_Widget):

    def __init__(self,config,parent):

        SCR_WDG_Widget.__init__(self,config,parent)

        self.table = SCR_WDG_Table(
                                    config=config, 
                                    search_clbk=None, 
                                    with_metadata=True, 
                                    model_class=SCR_WDG_EditorGrid_Model)

        self.messenger = SCR_Messenger()

        self.messenger.subscribe(
                                    "TestTreeSelectionChange",
                                    "SCR_WDG_EditorGrid",
                                    self.on_test_tree_selection_change)

    def populate(self):

        pass

        #self.table.populate(None,None)

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