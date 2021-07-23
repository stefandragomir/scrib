
from PyQt5.QtCore          import *
from PyQt5.QtGui           import *
from PyQt5.QtWidgets       import * 
from icons.icons           import SCR_GetIcon
from widgets.widgets       import SCR_WDG_Tree
from widgets.widgets       import SCR_WDG_Tree_Model
from widgets.widgets       import SCR_WDG_Tree_Item

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_TestTree_Model(SCR_WDG_Tree_Model):

    def __init__(self,parent):

        SCR_WDG_Tree_Model.__init__(self,parent)

    def load(self,data,parent):

        self.load_testfolder(data.testfolder,parent)

        self.load_external_resources(data.resources.external(),parent)
        
    def load_testsuite(self,data,parent):

        _labels = [
                    data.name,
                  ]

        _tree_testsuite = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                parent=parent)

        _tree_testsuite.icon     = "8e205a227046baee2a67b75fb12c95813784c484"
        _tree_testsuite.userdata = {"model":None}

        parent.add_child(_tree_testsuite)

        self.load_variables(data,_tree_testsuite)

        self.load_testcases(data,_tree_testsuite)

        self.load_keywords(data,_tree_testsuite)

    def load_testfolder(self,data,parent):

        _labels = [
                    data.name,
                  ]

        _tree_testfolder = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                parent=parent)

        _tree_testfolder.icon     = "585ba3e6f845cb67ef8a6098bed724e247278a5b"
        _tree_testfolder.userdata = {"model":None}

        for _testfolder in data.testfolders:

            self.load_testfolder(_testfolder,_tree_testfolder)

        for _testsuite in data.testsuites:

            self.load_testsuite(_testsuite,_tree_testfolder)

        for _resource in data.resources:

            self.load_resources(_resource,_tree_testfolder)

        if data.has_files():

            parent.add_child(_tree_testfolder)

    def load_testcases(self,data,parent):

        if data.model != None:

            for _section in data.model.sections:

                if data.is_section_testcases(_section):

                    for _testcase in _section.body:

                        self.load_testcase(_testcase,parent)

    def load_testcase(self,data,parent):

        _labels = [
                    data.name,
                  ]

        _tree_testcase = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                parent=parent)

        _tree_testcase.icon     = "ca211c47afa3b991350a6c183d8aaf3f33db15a0"
        _tree_testcase.userdata = {"model":None}

        parent.add_child(_tree_testcase)

    def load_variables(self,data,parent):

        if data.model != None:

            for _section in data.model.sections:

                if data.is_section_variables(_section):

                    for _variable in _section.body:

                        if data.is_statement_variable(_variable):

                            self.load_variable(_variable,parent)

    def load_variable(self,data,parent):

        _labels = [
                    data.name,
                  ]

        _tree_testcase = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                parent=parent)

        if data.name[0] == "$":
            _tree_testcase.icon     = "de99afcb2a785eea0974463ae9e7e063a5482b4a"
        elif data.name[0] == "@":
            _tree_testcase.icon     = "000cc208d4e675301e21ed009db52ff361a35a9f"
        elif data.name[0] == "&":
            _tree_testcase.icon     = "490daab16fc73f3decf083a5cfb04b47708c8b22"

        _tree_testcase.userdata = {"model":None}

        parent.add_child(_tree_testcase)

    def load_keywords(self,data,parent):

        if data.model != None:

            for _section in data.model.sections:

                if data.is_section_keywords(_section):

                    for _keyword in _section.body:

                        if data.is_statement_keyword(_keyword):

                            self.load_keyword(_keyword,parent)

    def load_keyword(self,data,parent):

        _labels = [
                    data.name,
                  ]

        _tree_keyword = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                parent=parent)

        _tree_keyword.icon     = "14b802564477e8b8f64dc869c92a4b983edc1001"
        _tree_keyword.userdata = {"model":None}

        parent.add_child(_tree_keyword)

    def load_resources(self,data,parent):

        _labels = [
                    data.name,
                  ]

        _tree_resource = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                parent=parent)

        _tree_resource.icon     = "26b41084d7c558d94b50f5e1c40cdfd362f05478"
        _tree_resource.userdata = {"model":None}

        parent.add_child(_tree_resource)

        self.load_variables(data,_tree_resource)

        self.load_keywords(data,_tree_resource)

    def load_external_resources(self,data,parent):

        _labels = ["External Resources"]

        _tree_ext_resources = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                parent=parent)

        _tree_ext_resources.icon     = "616b77c9b4e3020bee662e34c6feb5e8ddcd2b7d"
        _tree_ext_resources.userdata = {"model":None}

        parent.add_child(_tree_ext_resources)

        for _resource in data:

            self.load_resources(_resource,_tree_ext_resources)

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

