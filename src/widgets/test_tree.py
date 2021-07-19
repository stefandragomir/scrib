
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
                self.load_test_folder(data,parent)

    def load_test_suite(self,data,parent):

        _labels = [
                    data.name,
                  ]

        _tree_testsuite = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                parent=parent)

        _tree_testsuite.icon     = "8e205a227046baee2a67b75fb12c95813784c484"
        _tree_testsuite.userdata = {"model":None}

        parent.add_child(_tree_testsuite)

    def load_test_folder(self,data,parent):

        _labels = [
                    data.name,
                  ]

        _tree_testfolder = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                parent=parent)

        _tree_testfolder.icon     = "585ba3e6f845cb67ef8a6098bed724e247278a5b"
        _tree_testfolder.userdata = {"model":None}

        for _testfolder in data.testfolders:

            self.load_test_folder(_testfolder,_tree_testfolder)

        for _testsuite in data.testsuites:

            self.load_test_suite(_testsuite,_tree_testfolder)

        if data.has_files():

            parent.add_child(_tree_testfolder)

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

