
from PyQt5.QtCore          import *
from PyQt5.QtGui           import *
from PyQt5.QtWidgets       import * 
from icons.icons           import SCR_GetIcon
from widgets.widgets       import SCR_WDG_Tree
from widgets.widgets       import SCR_WDG_Tree_Model
from widgets.widgets       import SCR_WDG_Tree_Item
from control.control       import SCR_Control_TestSuite
from control.control       import SCR_Control_Folder

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_TestTree_Model(SCR_WDG_Tree_Model):

    def __init__(self,parent):

        SCR_WDG_Tree_Model.__init__(self,parent)

    def load(self,data,parent):

        if isinstance(data,SCR_Control_TestSuite):
            self.load_test_suite(data,parent)
        else:
            if isinstance(data,SCR_Control_Folder):
                print("SCR_Control_Folder")

    def load_test_suite(self,data,parent):

        _labels = [
                    data.name,
                  ]

        _tree_test_suite = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                parent=parent)

        _tree_test_suite.userdata = {"model":None}

        parent.add_child(_tree_test_suite)

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_TestTree(SCR_WDG_Tree):

    def __init__(self, config):

        SCR_WDG_Tree.__init__(
                                self,
                                config=config, 
                                usefind=True,
                                with_metadata=True,
                                model_class=SCR_WDG_TestTree_Model)

