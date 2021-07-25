
from PyQt5.QtCore          import *
from PyQt5.QtGui           import *
from PyQt5.QtWidgets       import * 
from icons.icons           import SCR_GetIcon
from widgets.widgets       import SCR_WDG_Tree
from widgets.widgets       import SCR_WDG_Tree_Model
from widgets.widgets       import SCR_WDG_Tree_Item
from widgets.widgets       import SCR_WDG_Selection


"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_Tree_Types():

    TESTFOLDER   = "testfolder"
    TESTSUITE    = "testsuite"
    TESTCASE     = "testcase"
    KEYWORD      = "keyword"
    VARIABLE     = "variable"
    RESOURCE     = "resource"
    LIBRARY      = "library"
    EXTRESOURCES = "extresources"
    EXTLIBRARIES = "extlibraries"

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_TestTree_Model(SCR_WDG_Tree_Model):

    def __init__(self,parent):

        SCR_WDG_Tree_Model.__init__(self,parent)

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
                                                parent=parent)

        _tree_testsuite.icon     = "8e205a227046baee2a67b75fb12c95813784c484"
        _tree_testsuite.userdata = {"model":data,"type": SCR_Tree_Types.TESTSUITE}

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
        _tree_testfolder.userdata = {"model":data,"type": SCR_Tree_Types.TESTFOLDER}

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
        _tree_testcase.userdata = {"model":data,"type": SCR_Tree_Types.TESTCASE}

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

        _tree_testcase.userdata = {"model":data,"type": SCR_Tree_Types.VARIABLE}

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
        _tree_keyword.userdata = {"model":data,"type": SCR_Tree_Types.KEYWORD}

        parent.add_child(_tree_keyword)

    def load_resources(self,data,parent):

        _labels = [
                    data.name,
                  ]

        _tree_resource = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                parent=parent)

        _tree_resource.icon     = "26b41084d7c558d94b50f5e1c40cdfd362f05478"
        _tree_resource.userdata = {"model":data,"type": SCR_Tree_Types.RESOURCE}

        parent.add_child(_tree_resource)

        self.load_variables(data,_tree_resource)

        self.load_keywords(data,_tree_resource)

    def load_libraries(self,data,parent):

        _labels = [
                    data.name,
                  ]

        _tree_library = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                parent=parent)

        _tree_library.icon     = "66a73259d66004e2b9c7180030bc347836ddcb82"
        _tree_library.userdata = {"model":data,"type": SCR_Tree_Types.LIBRARY}

        parent.add_child(_tree_library)

    def load_external_resources(self,data,parent):

        _labels = ["External Resources"]

        _tree_ext_resources = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                parent=parent)

        _tree_ext_resources.icon     = "616b77c9b4e3020bee662e34c6feb5e8ddcd2b7d"
        _tree_ext_resources.userdata = {"model":None,"type": SCR_Tree_Types.EXTRESOURCES}

        parent.add_child(_tree_ext_resources)

        for _resource in data:

            self.load_resources(_resource,_tree_ext_resources)

    def load_external_libraries(self,data,parent):

        _labels = ["External Libraries"]

        _tree_ext_libraries = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                parent=parent)

        _tree_ext_libraries.icon     = "66a73259d66004e2b9c7180030bc347836ddcb82"
        _tree_ext_libraries.userdata = {"model":None,"type":SCR_Tree_Types.EXTLIBRARIES}

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
        _name       = _index.data(Qt.DisplayRole)
        _user_data  = _index.data(Qt.UserRole)  

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

    def __init__(self, scrib, config, search_clbk):

        self.scrib = scrib

        SCR_WDG_Tree.__init__(
                                self,
                                config=config, 
                                search_clbk=search_clbk,
                                with_metadata=True,
                                model_class=SCR_WDG_TestTree_Model)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.draw_menu)

    def find_items_by_type(self,text,datatype):

        return self.custom_model.find_items_by_type(text,datatype)

    def draw_menu(self,point):

        self.menu_item =  self.indexAt(point)

        if self.menu_item:

            _user_data = self.get_user_data(self.menu_item)

            if _user_data != None:

                self.context_menu = QMenu()

                if _user_data["type"] == SCR_Tree_Types.TESTFOLDER:

                    self.draw_menu_testfolder()

                elif _user_data["type"] == SCR_Tree_Types.TESTSUITE:

                    self.draw_menu_testsuite()

                elif _user_data["type"] == SCR_Tree_Types.TESTCASE:

                    self.draw_menu_testcase()

                elif _user_data["type"] == SCR_Tree_Types.KEYWORD:

                    self.draw_menu_keyword()

                elif _user_data["type"] == SCR_Tree_Types.VARIABLE:

                    self.draw_menu_variable()

                elif _user_data["type"] == SCR_Tree_Types.RESOURCE:

                    self.draw_menu_resource()

                elif _user_data["type"] == SCR_Tree_Types.LIBRARY:

                    self.draw_menu_library()

                elif _user_data["type"] == SCR_Tree_Types.EXTRESOURCES:

                    self.draw_menu_ext_resources()

                elif _user_data["type"] == SCR_Tree_Types.EXTLIBRARIES:

                    self.draw_menu_ext_libraries()

                self.context_menu.exec_(self.mapToGlobal(point)) 

            else:
                self.context_menu = QMenu()

                self.context_menu.addAction(
                                            SCR_GetIcon("f12404a4b24f4ee746b13893bb7d7e9e67dafd97"), 
                                            "Search in Test Tree", 
                                            self.scrib.wdg_test_tree_find.show)

                self.context_menu.exec_(self.mapToGlobal(point)) 

    def draw_menu_testfolder(self):

        self.context_menu.addAction(
                                    SCR_GetIcon("8e205a227046baee2a67b75fb12c95813784c484"), 
                                    "New Test Suite", 
                                    lambda:None)

        self.context_menu.addAction(
                                    SCR_GetIcon("26b41084d7c558d94b50f5e1c40cdfd362f05478"), 
                                    "New Resource", 
                                    lambda:None)

        self.context_menu.addAction(
                                    SCR_GetIcon("66a73259d66004e2b9c7180030bc347836ddcb82"), 
                                    "New Library", 
                                    lambda:None)

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("c4c9e8e0c5587117224d03e1b36d2e25d9d096bb"), 
                                    "Delete", 
                                    lambda:None)

        self.context_menu.addAction(
                                    SCR_GetIcon("e7cec978fe0a220b390f534bc8060904b5a09293"), 
                                    "Rename", 
                                    lambda:None)

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("8c4ee08746e9d4d8b64596c87ac3fab1"), 
                                    "Expand", 
                                    lambda:None)

        self.context_menu.addAction(
                                    SCR_GetIcon("1022c7267f54abc54bd42a8b279d9180"), 
                                    "Collapse", 
                                    lambda:None)

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("b28971455cf45af0e2e37a9c33ca8ca01d5a660f"), 
                                    "Open Folder", 
                                    lambda:None)

        self.context_menu.addAction(
                                    SCR_GetIcon("f12404a4b24f4ee746b13893bb7d7e9e67dafd97"), 
                                    "Search in Folder", 
                                    lambda:None)

    def draw_menu_testsuite(self):

        self.context_menu.addAction(
                                    SCR_GetIcon("ca211c47afa3b991350a6c183d8aaf3f33db15a0"), 
                                    "New Test Case", 
                                    lambda:None)

        self.context_menu.addAction(
                                    SCR_GetIcon("14b802564477e8b8f64dc869c92a4b983edc1001"), 
                                    "New Keyword", 
                                    lambda:None)

        self.context_menu.addAction(
                                    SCR_GetIcon("de99afcb2a785eea0974463ae9e7e063a5482b4a"), 
                                    "New Scalar Variable", 
                                    lambda:None)

        self.context_menu.addAction(
                                    SCR_GetIcon("000cc208d4e675301e21ed009db52ff361a35a9f"), 
                                    "New List Variable", 
                                    lambda:None)

        self.context_menu.addAction(
                                    SCR_GetIcon("490daab16fc73f3decf083a5cfb04b47708c8b22"), 
                                    "New Dictionary Variable", 
                                    lambda:None)

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("836b4d076077202c00f2fbd10c605023bb2bbfe5"), 
                                    "Select All Test Cases", 
                                    lambda:None)

        self.context_menu.addAction(
                                    SCR_GetIcon("a2588e1c2a378b9710d5a1b74299060ca2271413"), 
                                    "Select All Failed Test Cases", 
                                    lambda:None)

        self.context_menu.addAction(
                                    SCR_GetIcon("8bd133d5a6e9b47ba80a6d774149085b20483fb0"), 
                                    "Select All Passed Test Cases", 
                                    lambda:None)

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("c4c9e8e0c5587117224d03e1b36d2e25d9d096bb"), 
                                    "Delete", 
                                    lambda:None)

        self.context_menu.addAction(
                                    SCR_GetIcon("e7cec978fe0a220b390f534bc8060904b5a09293"), 
                                    "Rename", 
                                    lambda:None)

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("f12404a4b24f4ee746b13893bb7d7e9e67dafd97"), 
                                    "Search in Test Suite", 
                                    lambda:None)

    def draw_menu_testcase(self):


        self.context_menu.addAction(
                                    SCR_GetIcon("c4c9e8e0c5587117224d03e1b36d2e25d9d096bb"), 
                                    "Delete", 
                                    lambda:None)

        self.context_menu.addAction(
                                    SCR_GetIcon("e7cec978fe0a220b390f534bc8060904b5a09293"), 
                                    "Rename", 
                                    lambda:None)

    def draw_menu_keyword(self):

        self.context_menu.addAction(
                                    SCR_GetIcon("fd2cf51bcbd304d61dbae1fdd954d4d1ec41e535"), 
                                    "Delete", 
                                    lambda:None)

        self.context_menu.addAction(
                                    SCR_GetIcon("fd2cf51bcbd304d61dbae1fdd954d4d1ec41e535"), 
                                    "Rename", 
                                    lambda:None)

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("ffc3fb09c5db2b34f971c0ec4979b73de4f14be5"), 
                                    "Find Usage", 
                                    lambda:None)

    def draw_menu_variable(self):

        self.context_menu.addAction(
                                    SCR_GetIcon("c4c9e8e0c5587117224d03e1b36d2e25d9d096bb"), 
                                    "Delete", 
                                    lambda:None)

        self.context_menu.addAction(
                                    SCR_GetIcon("e7cec978fe0a220b390f534bc8060904b5a09293"), 
                                    "Rename", 
                                    lambda:None)

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("ffc3fb09c5db2b34f971c0ec4979b73de4f14be5"), 
                                    "Find Usage", 
                                    lambda:None)

    def draw_menu_resource(self):

        self.context_menu.addAction(
                                    SCR_GetIcon("14b802564477e8b8f64dc869c92a4b983edc1001"), 
                                    "New Keyword", 
                                    lambda:None)

        self.context_menu.addAction(
                                    SCR_GetIcon("de99afcb2a785eea0974463ae9e7e063a5482b4a"), 
                                    "New Scalar Variable", 
                                    lambda:None)

        self.context_menu.addAction(
                                    SCR_GetIcon("000cc208d4e675301e21ed009db52ff361a35a9f"), 
                                    "New List Variable", 
                                    lambda:None)

        self.context_menu.addAction(
                                    SCR_GetIcon("490daab16fc73f3decf083a5cfb04b47708c8b22"), 
                                    "New Dictionary Variable", 
                                    lambda:None)

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("c4c9e8e0c5587117224d03e1b36d2e25d9d096bb"), 
                                    "Delete", 
                                    lambda:None)

        self.context_menu.addAction(
                                    SCR_GetIcon("e7cec978fe0a220b390f534bc8060904b5a09293"), 
                                    "Rename", 
                                    lambda:None)

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("f12404a4b24f4ee746b13893bb7d7e9e67dafd97"), 
                                    "Search in Resource", 
                                    lambda:None)

        self.context_menu.addAction(
                                    SCR_GetIcon("ffc3fb09c5db2b34f971c0ec4979b73de4f14be5"), 
                                    "Find Usage", 
                                    lambda:None)

    def draw_menu_library(self):

        self.context_menu.addAction(
                                    SCR_GetIcon("c4c9e8e0c5587117224d03e1b36d2e25d9d096bb"), 
                                    "Delete", 
                                    lambda:None)

        self.context_menu.addAction(
                                    SCR_GetIcon("e7cec978fe0a220b390f534bc8060904b5a09293"), 
                                    "Rename", 
                                    lambda:None)

        self.context_menu.addSeparator()

        self.context_menu.addAction(
                                    SCR_GetIcon("ffc3fb09c5db2b34f971c0ec4979b73de4f14be5"), 
                                    "Find Usage", 
                                    lambda:None)

    def draw_menu_ext_resources(self):

        self.context_menu.addAction(
                                    SCR_GetIcon("f12404a4b24f4ee746b13893bb7d7e9e67dafd97"), 
                                    "Search in External Resource", 
                                    lambda:None)

    def draw_menu_ext_libraries(self):

        self.context_menu.addAction(
                                    SCR_GetIcon("f12404a4b24f4ee746b13893bb7d7e9e67dafd97"), 
                                    "Search in External Libraries", 
                                    lambda:None)

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_TestTree_Find(QWidget):

    def __init__(self,config,tree):

        QWidget.__init__(self,tree)

        self.config = config

        self._items          = []
        self._item_idx       = 0
        self._text_changed   = False
        self.tree            = tree
        self.selection_type  = "all"  
            
        #write line
        self.line = QLineEdit()
        self.line.setContextMenuPolicy(Qt.NoContextMenu)    
        self.line.setStyleSheet('border: 1px solid gray;')
        self.line.returnPressed.connect(self._find_next) 
        self.line.textEdited.connect(self._textedited)

        #find previous button
        self._find_prev_button = QToolButton()
        self._find_prev_button.setStyleSheet("background: transparent; border-radius: 0px")
        self._find_prev_button.setIcon(SCR_GetIcon('85905e29412dc4ee1bca3b78beeca05a0ea1d14b'))
        self._find_prev_button.setToolTip("Find Previous Item")
        self._find_prev_button.clicked.connect(self._find_prev)                 

        #find next button
        self._find_next_button = QToolButton()
        self._find_next_button.setStyleSheet("background: transparent; border-radius: 0px")
        self._find_next_button.setIcon(SCR_GetIcon('47d97a19678ecbc93257bfc890b71cc62f4ae908'))
        self._find_prev_button.setToolTip("Find Next Item")
        self._find_next_button.clicked.connect(self._find_next)           

        #close button
        self._close_button = QToolButton()
        self._close_button.setStyleSheet("background: transparent; border-radius: 0px")
        self._close_button.setIcon(SCR_GetIcon('779d79bcda4833c45d97b063d0041af2e47265e4'))
        self._find_prev_button.setToolTip("Close Test Tree Search Bar")
        self._close_button.clicked.connect(self.hide)

        #type selection
        self._selection = SCR_WDG_Selection(self.config)
        self._selection.setFixedWidth(80)
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

        box = QHBoxLayout(self)
        box.addWidget(self.line)
        box.addWidget(self._selection)
        box.addWidget(self._find_next_button)
        box.addWidget(self._find_prev_button)        
        box.addWidget(self._close_button)
        box.setSizeConstraint(3)
        box.setContentsMargins(8, 8, 5, 5)
        self.setLayout(box)

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