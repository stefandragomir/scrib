"""
File contains all UI widgets regarding the Test Tree
"""

from PyQt6.QtCore          import *
from PyQt6.QtGui           import *
from PyQt6.QtWidgets       import * 
from icons.icons           import SCR_GetIcon
from widgets.widgets       import SCR_WDG_Tree
from widgets.widgets       import SCR_WDG_Tree_Model
from widgets.widgets       import SCR_WDG_Tree_Item
from widgets.widgets       import SCR_WDG_Selection
from widgets.widgets       import SCR_WDG_Widget
from widgets.widgets       import SCR_WDG_LineEdit
from widgets.widgets       import SCR_WDG_ToolButton
from actions.actions       import SCR_Actions_Tree_TestFolder
from actions.actions       import SCR_Actions_Tree_TestSuite
from actions.actions       import SCR_Actions_Tree_Resource
from actions.actions       import SCR_Actions_Tree_TestCase
from actions.actions       import SCR_Actions_Tree_Keyword
from actions.actions       import SCR_Actions_Tree_Variable
from actions.actions       import SCR_Actions_Tree_Library
from actions.actions       import SCR_Actions_Tree_ExtResources
from actions.actions       import SCR_Actions_Tree_ExtLibraries
from functools             import partial


"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_TestTree_Widget(SCR_WDG_Widget):

    def __init__(self,config, scrib):

        SCR_WDG_Widget.__init__(self,config)

        self.scrib  = scrib 
        self.config = config

        self.draw()

    def draw(self):

        self.ly = QVBoxLayout()

        self.wdg_tree = SCR_WDG_TestTree(self.config,self.scrib,lambda:self.wdg_search.show())

        self.wdg_tree.setHeaderHidden(True)

        _policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        _policy.setHorizontalStretch(1)

        self.wdg_tree.setSizePolicy(_policy)

        self.wdg_search = SCR_WDG_TestTree_Find(self.config,self.wdg_tree)

        self.wdg_search.hide()

        self.ly.addWidget(self.wdg_tree)
        self.ly.addWidget(self.wdg_search)

        self.setLayout(self.ly)

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_Tree_Types():

    TESTFOLDER   = "testfolder"
    TESTSUITE    = "testsuite"
    TESTCASE     = "testcase"
    KEYWORDS     = "keywords"
    KEYWORD      = "keyword"
    VARIABLES    = "variables"
    VARIABLE     = "variable"
    RESOURCE     = "resource"
    LIBRARY      = "library"
    EXTRESOURCES = "extresources"
    EXTLIBRARIES = "extlibraries"

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_TestTree_Model(SCR_WDG_Tree_Model):

    def __init__(self,config,parent):

        SCR_WDG_Tree_Model.__init__(self,config,parent)

    def load(self,data,parent):

        self.load_testfolder(data.testfolder,parent)

        self.load_external_resources(data.resources.external(),parent)

        self.load_external_libraries(data.libraries.external(),parent)
        
    def load_testsuite(self,data,parent):

        _labels = [
                    data.name,
                  ]

        _tree_testsuite = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                config=self.config,
                                                parent=parent)

        _tree_testsuite.icon     = self.config.get_theme_icon_testsuite()
        _tree_testsuite.userdata = {"data":data,"type": SCR_Tree_Types.TESTSUITE}

        parent.add_child(_tree_testsuite)

        self.load_testcases(data,_tree_testsuite)

        self.load_variables(data,_tree_testsuite)        

        self.load_keywords(data,_tree_testsuite)

    def load_testfolder(self,data,parent):

        _labels = [
                    data.name,
                  ]

        _tree_testfolder = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                config=self.config,
                                                parent=parent)

        _tree_testfolder.icon     = self.config.get_theme_icon_folder()
        _tree_testfolder.userdata = {"data":data,"type": SCR_Tree_Types.TESTFOLDER}

        for _testfolder in data.testfolders:

            self.load_testfolder(_testfolder,_tree_testfolder)

        for _testsuite in data.testsuites:

            self.load_testsuite(_testsuite,_tree_testfolder)

        for _resource in data.resources:

            self.load_resources(_resource,_tree_testfolder)

        for _library in data.libraries:

            self.load_libraries(_library,_tree_testfolder)

        if data.has_files():

            parent.add_child(_tree_testfolder)

    def load_testcases(self,data,parent):

        if data != None:

            for _testcase in data.testcases:

                self.load_testcase(_testcase,parent)

    def load_testcase(self,data,parent):

        _labels = [
                    data.name,
                  ]

        _tree_testcase = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                config=self.config,
                                                parent=parent)

        _tree_testcase.icon     = self.config.get_theme_icon_testcase()
        _tree_testcase.userdata = {"data":data,"type": SCR_Tree_Types.TESTCASE}

        parent.add_child(_tree_testcase)

    def load_variables(self,data,parent):

        if data != None:

            _labels = [
                        "Variables",
                      ]

            _tree_variables = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                config=self.config,
                                                parent=parent)

            _tree_variables.icon     = self.config.get_theme_icon_folder_variables()
           
            _tree_variables.userdata = {"data":data,"type": SCR_Tree_Types.VARIABLES}

            parent.add_child(_tree_variables)

            for _variable in data.variables:

                self.load_variable(_variable,_tree_variables)

    def load_variable(self,data,parent):

        _labels = [
                    data.name,
                  ]

        _tree_variable = SCR_WDG_Tree_Item(
                                            data=_labels,
                                            config=self.config,
                                            parent=parent)

        if data.name[0] == "$":
            _tree_variable.icon     = self.config.get_theme_icon_var_scalar()
        elif data.name[0] == "@":
            _tree_variable.icon     = self.config.get_theme_icon_var_list()
        elif data.name[0] == "&":
            _tree_variable.icon     = self.config.get_theme_icon_var_dict()

        _tree_variable.userdata = {"data":data,"type": SCR_Tree_Types.VARIABLE}

        parent.add_child(_tree_variable)

    def load_keywords(self,data,parent):

        if data != None:

            _labels = [
                        "Keywords",
                      ]

            _tree_keywords = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                config=self.config,
                                                parent=parent)

            _tree_keywords.icon     = self.config.get_theme_icon_folder_keywords()
           
            _tree_keywords.userdata = {"data":data,"type": SCR_Tree_Types.KEYWORDS}

            parent.add_child(_tree_keywords)

            for _keyword in data.keywords:

                self.load_keyword(_keyword,_tree_keywords)

    def load_keyword(self,data,parent):

        _labels = [
                    data.name,
                  ]

        _tree_keyword = SCR_WDG_Tree_Item(
                                            data=_labels,
                                            config=self.config,
                                            parent=parent)

        _tree_keyword.icon     = self.config.get_theme_icon_keyword()
        _tree_keyword.userdata = {"data":data,"type": SCR_Tree_Types.KEYWORD}

        parent.add_child(_tree_keyword)

    def load_resources(self,data,parent):

        _labels = [
                    data.name,
                  ]

        _tree_resource = SCR_WDG_Tree_Item(
                                            data=_labels,
                                            config=self.config,
                                            parent=parent)

        _tree_resource.icon     = self.config.get_theme_icon_resource()
        _tree_resource.userdata = {"data":data,"type": SCR_Tree_Types.RESOURCE}

        parent.add_child(_tree_resource)

        self.load_variables(data,_tree_resource)

        self.load_keywords(data,_tree_resource)

    def load_libraries(self,data,parent):

        _labels = [
                    data.name,
                  ]

        _tree_library = SCR_WDG_Tree_Item(
                                            data=_labels,
                                            config=self.config,
                                            parent=parent)

        _tree_library.icon     = self.config.get_theme_icon_python()
        _tree_library.userdata = {"data":data,"type": SCR_Tree_Types.LIBRARY}

        parent.add_child(_tree_library)

    def load_external_resources(self,data,parent):

        _labels = ["External Resources"]

        _tree_ext_resources = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                config=self.config,
                                                parent=parent)

        _tree_ext_resources.icon     = self.config.get_theme_icon_folder()
        _tree_ext_resources.userdata = {"data":None,"type": SCR_Tree_Types.EXTRESOURCES}

        parent.add_child(_tree_ext_resources)

        for _resource in data:

            self.load_resources(_resource,_tree_ext_resources)

    def load_external_libraries(self,data,parent):

        _labels = ["External Libraries"]

        _tree_ext_libraries = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                config=self.config,
                                                parent=parent)

        _tree_ext_libraries.icon     = self.config.get_theme_icon_python()
        _tree_ext_libraries.userdata = {"data":None,"type":SCR_Tree_Types.EXTLIBRARIES}

        parent.add_child(_tree_ext_libraries)

        for _resource in data:

            self.load_libraries(_resource,_tree_ext_libraries)

    def find_items_by_type(self,text,datatype):

        _items = []

        if self.root != None:

            for _row in range(self.root.child_count()):

                _items += self.find(
                                    _row,
                                    text,
                                    QModelIndex(),
                                    datatype)

        return _items

    def find(self,row,text,parent,datatype):

        _finds      = []
        _index      = self.index(row, 0, parent)
        _name       = _index.data(Qt.ItemDataRole.DisplayRole)
        _user_data  = _index.data(Qt.ItemDataRole.UserRole)  

        if text.lower() in _name.lower():

            if "all" == datatype:
                _finds.append(_index)
            else:
                if _user_data["type"] == datatype:
                    _finds.append(_index)

        _index_root = self.index(row, 0, parent)

        for _child_row in range(self.rowCount(_index_root)):

            _finds += self.find(
                                _child_row, 
                                text, 
                                _index_root,
                                datatype)

        return _finds

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_TestTree(SCR_WDG_Tree):

    def __init__(self, config, scrib, search_clbk):

        self.scrib             = scrib
        self.act_testfolder    = SCR_Actions_Tree_TestFolder(self.scrib)
        self.act_testsuite     = SCR_Actions_Tree_TestSuite(self.scrib)
        self.act_resource      = SCR_Actions_Tree_Resource(self.scrib)
        self.act_testcase      = SCR_Actions_Tree_TestCase(self.scrib)
        self.act_keyword       = SCR_Actions_Tree_Keyword(self.scrib)
        self.act_variable      = SCR_Actions_Tree_Variable(self.scrib)
        self.act_library       = SCR_Actions_Tree_Library(self.scrib)
        self.act_ext_resources = SCR_Actions_Tree_ExtResources(self.scrib)
        self.act_ext_libraries = SCR_Actions_Tree_ExtLibraries(self.scrib)

        SCR_WDG_Tree.__init__(
                                self,
                                config=config, 
                                search_clbk=search_clbk,
                                with_metadata=True,
                                model_class=SCR_WDG_TestTree_Model)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.draw_menu)

    def find_items_by_type(self,text,datatype):

        return self.custom_model.find_items_by_type(text,datatype)

    def draw_menu(self,point):

        self.tree_item =  self.indexAt(point)

        if self.tree_item:

            _user_data = self.get_user_data(self.tree_item)

            if _user_data != None:

                self.context_menu = QMenu()

                if _user_data["type"] == SCR_Tree_Types.TESTFOLDER:

                    self.draw_menu_testfolder(_user_data["data"])

                elif _user_data["type"] == SCR_Tree_Types.TESTSUITE:

                    self.draw_menu_testsuite(_user_data["data"])

                elif _user_data["type"] == SCR_Tree_Types.TESTCASE:

                    self.draw_menu_testcase(_user_data["data"])

                elif _user_data["type"] == SCR_Tree_Types.KEYWORD:

                    self.draw_menu_keyword(_user_data["data"])

                elif _user_data["type"] == SCR_Tree_Types.VARIABLE:

                    self.draw_menu_variable(_user_data["data"])

                elif _user_data["type"] == SCR_Tree_Types.RESOURCE:

                    self.draw_menu_resource(_user_data["data"])

                elif _user_data["type"] == SCR_Tree_Types.LIBRARY:

                    self.draw_menu_library(_user_data["data"])

                elif _user_data["type"] == SCR_Tree_Types.EXTRESOURCES:

                    self.draw_menu_ext_resources(_user_data["data"])

                elif _user_data["type"] == SCR_Tree_Types.EXTLIBRARIES:

                    self.draw_menu_ext_libraries(_user_data["data"])

                self.context_menu.exec(self.mapToGlobal(point)) 

            else:
                self.context_menu = QMenu()

                self.context_menu.addAction(
                                            SCR_GetIcon("f12404a4b24f4ee746b13893bb7d7e9e67dafd97"), 
                                            "Search in Test Tree", 
                                            self.scrib.wdg_test_tree_find.show)

                self.context_menu.exec(self.mapToGlobal(point)) 

    def draw_menu_testfolder(self,data):

        self.context_menu.addAction(
                                    SCR_GetIcon("8e205a227046baee2a67b75fb12c95813784c484"), 
                                    "New Test Suite", 
                                    partial(self.act_testfolder.new_test_suite,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("26b41084d7c558d94b50f5e1c40cdfd362f05478"), 
                                    "New Resource", 
                                    partial(self.act_testfolder.new_resource,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("66a73259d66004e2b9c7180030bc347836ddcb82"), 
                                    "New Library", 
                                    partial(self.act_testfolder.new_library,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("585ba3e6f845cb67ef8a6098bed724e247278a5b"), 
                                    "New Folder", 
                                    partial(self.act_testfolder.new_folder,self.tree_item,data))

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("c4c9e8e0c5587117224d03e1b36d2e25d9d096bb"), 
                                    "Delete", 
                                    partial(self.act_testfolder.delete,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("e7cec978fe0a220b390f534bc8060904b5a09293"), 
                                    "Rename", 
                                    partial(self.act_testfolder.rename,self.tree_item,data))

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("836b4d076077202c00f2fbd10c605023bb2bbfe5"), 
                                    "Select All Test Cases", 
                                    partial(self.act_testfolder.sel_all,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("98e83543511ae234092459c5450e0d0dee23337d"), 
                                    "Select All Failed Test Cases", 
                                    partial(self.act_testfolder.sel_all_failed,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("a37bb6398d3f69a8f2914f3cdcb209fbf2e2cfc7"), 
                                    "Select All Passed Test Cases", 
                                    partial(self.act_testfolder.sel_all_passed,self.tree_item,data))

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("b49bc191b2a8c689d3d25431dde459e769349b8f"), 
                                    "Deselect All Test Cases", 
                                    partial(self.act_testfolder.desel_all,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("a2588e1c2a378b9710d5a1b74299060ca2271413"), 
                                    "Deselect All Failed Test Cases", 
                                    partial(self.act_testfolder.desel_all_failed,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("8bd133d5a6e9b47ba80a6d774149085b20483fb0"), 
                                    "Deselect All Passed Test Cases", 
                                    partial(self.act_testfolder.desel_all_passed,self.tree_item,data))

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("8c4ee08746e9d4d8b64596c87ac3fab1"), 
                                    "Expand", 
                                    partial(self.expandChildren,self.tree_item))

        self.context_menu.addAction(
                                    SCR_GetIcon("1022c7267f54abc54bd42a8b279d9180"), 
                                    "Collapse", 
                                    partial(self.collapseChildren,self.tree_item))

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("b28971455cf45af0e2e37a9c33ca8ca01d5a660f"), 
                                    "Open Folder", 
                                    partial(self.act_testfolder.open,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("f12404a4b24f4ee746b13893bb7d7e9e67dafd97"), 
                                    "Search in Folder", 
                                    partial(self.act_testfolder.search,self.tree_item,data))

    def draw_menu_testsuite(self,data):

        self.context_menu.addAction(
                                    SCR_GetIcon("ca211c47afa3b991350a6c183d8aaf3f33db15a0"), 
                                    "New Test Case", 
                                    partial(self.act_testsuite.new_testcase,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("14b802564477e8b8f64dc869c92a4b983edc1001"), 
                                    "New Keyword", 
                                    partial(self.act_testsuite.new_keyword,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("de99afcb2a785eea0974463ae9e7e063a5482b4a"), 
                                    "New Scalar Variable", 
                                    partial(self.act_testsuite.new_var_scalar,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("000cc208d4e675301e21ed009db52ff361a35a9f"), 
                                    "New List Variable", 
                                    partial(self.act_testsuite.new_var_list,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("490daab16fc73f3decf083a5cfb04b47708c8b22"), 
                                    "New Dictionary Variable", 
                                    partial(self.act_testsuite.new_var_dict,self.tree_item,data))

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("836b4d076077202c00f2fbd10c605023bb2bbfe5"), 
                                    "Select All Test Cases", 
                                    partial(self.act_testsuite.sel_all,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("98e83543511ae234092459c5450e0d0dee23337d"), 
                                    "Select All Failed Test Cases", 
                                    partial(self.act_testsuite.sel_all_failed,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("a37bb6398d3f69a8f2914f3cdcb209fbf2e2cfc7"), 
                                    "Select All Passed Test Cases", 
                                    partial(self.act_testsuite.sel_all_passed,self.tree_item,data))

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("b49bc191b2a8c689d3d25431dde459e769349b8f"), 
                                    "Deselect All Test Cases", 
                                    partial(self.act_testsuite.desel_all,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("a2588e1c2a378b9710d5a1b74299060ca2271413"), 
                                    "Deselect All Failed Test Cases", 
                                    partial(self.act_testsuite.desel_all_failed,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("8bd133d5a6e9b47ba80a6d774149085b20483fb0"), 
                                    "Deselect All Passed Test Cases", 
                                    partial(self.act_testsuite.desel_all_passed,self.tree_item,data))


        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("c4c9e8e0c5587117224d03e1b36d2e25d9d096bb"), 
                                    "Delete", 
                                    partial(self.act_testsuite.delete,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("e7cec978fe0a220b390f534bc8060904b5a09293"), 
                                    "Rename", 
                                    partial(self.act_testsuite.rename,self.tree_item,data))

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("b28971455cf45af0e2e37a9c33ca8ca01d5a660f"), 
                                    "Open Folder", 
                                    partial(self.act_testsuite.open,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("f12404a4b24f4ee746b13893bb7d7e9e67dafd97"), 
                                    "Search in Test Suite", 
                                    partial(self.act_testsuite.search,self.tree_item,data))

    def draw_menu_testcase(self,data):


        self.context_menu.addAction(
                                    SCR_GetIcon("c4c9e8e0c5587117224d03e1b36d2e25d9d096bb"), 
                                    "Delete", 
                                    partial(self.act_testcase.delete,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("e7cec978fe0a220b390f534bc8060904b5a09293"), 
                                    "Rename", 
                                    partial(self.act_testcase.rename,self.tree_item,data))

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("85d95f3e36517321283568bf441922f4cfe53ec1"), 
                                    "Move Up", 
                                    partial(self.act_testcase.moveup,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("8cb8f5436aebe089cb7a9fe81a909675847e0c81"), 
                                    "Move Down", 
                                    partial(self.act_testcase.movedown,self.tree_item,data))

    def draw_menu_keyword(self,data):

        self.context_menu.addAction(
                                    SCR_GetIcon("c4c9e8e0c5587117224d03e1b36d2e25d9d096bb"), 
                                    "Delete", 
                                    partial(self.act_keyword.delete,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("e7cec978fe0a220b390f534bc8060904b5a09293"), 
                                    "Rename", 
                                    partial(self.act_keyword.rename,self.tree_item,data))

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("85d95f3e36517321283568bf441922f4cfe53ec1"), 
                                    "Move Up", 
                                    partial(self.act_keyword.moveup,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("8cb8f5436aebe089cb7a9fe81a909675847e0c81"), 
                                    "Move Down", 
                                    partial(self.act_keyword.movedown,self.tree_item,data))

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("ffc3fb09c5db2b34f971c0ec4979b73de4f14be5"), 
                                    "Find Usage", 
                                    partial(self.act_keyword.find_usage,self.tree_item,data))

    def draw_menu_variable(self,data):

        self.context_menu.addAction(
                                    SCR_GetIcon("c4c9e8e0c5587117224d03e1b36d2e25d9d096bb"), 
                                    "Delete", 
                                    partial(self.act_variable.delete,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("e7cec978fe0a220b390f534bc8060904b5a09293"), 
                                    "Rename", 
                                    partial(self.act_variable.rename,self.tree_item,data))

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("85d95f3e36517321283568bf441922f4cfe53ec1"), 
                                    "Move Up", 
                                    partial(self.act_variable.moveup,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("8cb8f5436aebe089cb7a9fe81a909675847e0c81"), 
                                    "Move Down", 
                                    partial(self.act_variable.movedown,self.tree_item,data))

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("ffc3fb09c5db2b34f971c0ec4979b73de4f14be5"), 
                                    "Find Usage", 
                                    partial(self.act_variable.find_usage,self.tree_item,data))

    def draw_menu_resource(self,data):

        self.context_menu.addAction(
                                    SCR_GetIcon("14b802564477e8b8f64dc869c92a4b983edc1001"), 
                                    "New Keyword", 
                                    partial(self.act_resource.new_keyword,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("de99afcb2a785eea0974463ae9e7e063a5482b4a"), 
                                    "New Scalar Variable", 
                                    partial(self.act_resource.new_var_scalar,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("000cc208d4e675301e21ed009db52ff361a35a9f"), 
                                    "New List Variable", 
                                    partial(self.act_resource.new_var_list,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("490daab16fc73f3decf083a5cfb04b47708c8b22"), 
                                    "New Dictionary Variable", 
                                    partial(self.act_resource.new_var_dict,self.tree_item,data))

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("c4c9e8e0c5587117224d03e1b36d2e25d9d096bb"), 
                                    "Delete", 
                                    partial(self.act_resource.delete,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("e7cec978fe0a220b390f534bc8060904b5a09293"), 
                                    "Rename", 
                                    partial(self.act_resource.rename,self.tree_item,data))

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("b28971455cf45af0e2e37a9c33ca8ca01d5a660f"), 
                                    "Open Folder", 
                                    partial(self.act_resource.open,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("f12404a4b24f4ee746b13893bb7d7e9e67dafd97"), 
                                    "Search in Resource", 
                                    partial(self.act_resource.search,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("ffc3fb09c5db2b34f971c0ec4979b73de4f14be5"), 
                                    "Find Usage", 
                                    partial(self.act_resource.find_usage,self.tree_item,data))

    def draw_menu_library(self,data):

        self.context_menu.addAction(
                                    SCR_GetIcon("c4c9e8e0c5587117224d03e1b36d2e25d9d096bb"), 
                                    "Delete", 
                                    partial(self.act_library.delete,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("e7cec978fe0a220b390f534bc8060904b5a09293"), 
                                    "Rename", 
                                    partial(self.act_library.rename,self.tree_item,data))

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("b28971455cf45af0e2e37a9c33ca8ca01d5a660f"), 
                                    "Open Folder", 
                                    partial(self.act_library.open,self.tree_item,data))

        self.context_menu.addAction(
                                    SCR_GetIcon("ffc3fb09c5db2b34f971c0ec4979b73de4f14be5"), 
                                    "Find Usage", 
                                    partial(self.act_library.find_usage,self.tree_item,data))

    def draw_menu_ext_resources(self,data):

        self.context_menu.addAction(
                                    SCR_GetIcon("f12404a4b24f4ee746b13893bb7d7e9e67dafd97"), 
                                    "Search in External Resource", 
                                    partial(self.act_ext_resources.search,self.tree_item,data))

    def draw_menu_ext_libraries(self,data):

        self.context_menu.addAction(
                                    SCR_GetIcon("f12404a4b24f4ee746b13893bb7d7e9e67dafd97"), 
                                    "Search in External Libraries", 
                                    partial(self.act_ext_libraries.search,self.tree_item,data))

    def create_item(self,parent,text):

        _new_item = self.custom_model.insertRow(0, parent, text)

        self.scrollToItem(_new_item)

        self.selectionModel().clear()

        self.selectionModel().select(_new_item,QItemSelectionModel.Select)

        self.edit(_new_item)

        self.itemDelegate().closeEditor.connect(self.edit_done)

    def edit_done(self,editor):

        print("activated")

    def selectionChanged(self,selected,deselected):

        if selected.indexes():

            for _item_index in selected.indexes():

                _data = self.custom_model.data(_item_index,Qt.ItemDataRole.UserRole)

                if _data["data"] != None:

                    _status_bar_label = _data["data"].get_status_label()

                    self.scrib.status_bar.label(_status_bar_label)
        
"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_TestTree_Find(SCR_WDG_Widget):

    def __init__(self,config,tree):

        SCR_WDG_Widget.__init__(self,config,tree)

        self.config = config

        self._items          = []
        self._item_idx       = 0
        self._text_changed   = False
        self.tree            = tree
        self.selection_type  = "all"  
            
        #write line
        self.line = SCR_WDG_LineEdit(self.config)
        self.line.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)    
        self.line.setStyleSheet('border: 1px solid gray;')
        self.line.returnPressed.connect(self._find_next)
        self.line.textEdited.connect(self._textedited)

        #find previous button
        self._find_prev_button = SCR_WDG_ToolButton(self.config)
        self._find_prev_button.setStyleSheet("background: transparent; border-radius: 0px")
        self._find_prev_button.setIcon(SCR_GetIcon(self.config.get_theme_icon_previous()))
        self._find_prev_button.setToolTip("Find Previous Item")
        self._find_prev_button.clicked.connect(self._find_prev)                 

        #find next button
        self._find_next_button = SCR_WDG_ToolButton(self.config)
        self._find_next_button.setStyleSheet("background: transparent; border-radius: 0px")
        self._find_next_button.setIcon(SCR_GetIcon(self.config.get_theme_icon_next()))
        self._find_prev_button.setToolTip("Find Next Item")
        self._find_next_button.clicked.connect(self._find_next)           

        #close button
        self._close_button = SCR_WDG_ToolButton(self.config)
        self._close_button.setStyleSheet("background: transparent; border-radius: 0px")
        self._close_button.setIcon(SCR_GetIcon(self.config.get_theme_icon_close()))
        self._find_prev_button.setToolTip("Close Test Tree Search Bar")
        self._close_button.clicked.connect(self.hide)

        #type selection
        self._selection = SCR_WDG_Selection(self.config)
        self._selection.setFixedWidth(90)
        self._selection.setStyleSheet('border: 1px solid gray;')
        self._selection.currentIndexChanged.connect(self.selection_change)

        _data = [
                    {"All"       : "all"                     },
                    {"Test Suite": SCR_Tree_Types.TESTSUITE  },
                    {"Test Case" : SCR_Tree_Types.TESTCASE   },
                    {"Keyword"   : SCR_Tree_Types.KEYWORD    },
                    {"Variable"  : SCR_Tree_Types.VARIABLE   },
                    {"Folder"    : SCR_Tree_Types.TESTFOLDER },
                    {"Resource"  : SCR_Tree_Types.RESOURCE   },
                    {"Library"   : SCR_Tree_Types.LIBRARY    },
                ] 

        self._selection.populate(_data)

        _vly = QVBoxLayout(self)

        _hly = QHBoxLayout()
        _hly.addWidget(self._selection)
        _hly.addWidget(self._find_next_button)
        _hly.addWidget(self._find_prev_button)        
        _hly.addWidget(self._close_button)
        _hly.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        _hly.setContentsMargins(8, 8, 5, 5)
        
        _vly.addWidget(self.line)
        _vly.addLayout(_hly)

        self.setLayout(_vly)

    def selection_change(self):

        self.selection_type = self._selection.get_item_data(self._selection.currentText())

        self._text_changed = True

    def _textedited(self):

        self._text_changed = True
        self._item_idx     = 0

    def go_to_item(self,item):

        if item != None:

            self.tree.scrollToItem(item)
            self.tree.setCurrentIndex(item)

            if item.parent():

                self.tree.expand(item)        

            self.tree.setFocus()

    def _find_next(self):

        _item = None

        if self.word.strip() != "":

            if self._text_changed:

                self._items = self.tree.find_items_by_type(self.word, self.selection_type)

                self._text_changed = False

            if self._item_idx < len(self._items) and self._item_idx >= 0:

                _item           = self._items[self._item_idx]   
                self._item_idx += 1
            else:
                _item = None

            self.go_to_item(_item)               

    def _find_prev(self):

        _item = None

        if self.word.strip() != "":

            if self._text_changed:

                self._items = self.tree.find_items_by_type(self.word, self.selection_type)

                self._text_changed = False

            if self._item_idx <= len(self._items) and self._item_idx >= 1:

                self._item_idx -= 1
                _item           = self._items[self._item_idx]   
                
            else:
                _item = None

            self.go_to_item(_item)   

    @property
    def word(self):

        return str(self.line.text())