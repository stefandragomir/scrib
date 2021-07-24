
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
        _tree_testsuite.userdata = {"model":data,"type": "testsuite"}

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
        _tree_testfolder.userdata = {"model":data,"type": "testfolder"}

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
        _tree_testcase.userdata = {"model":data,"type": "testcase"}

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

        _tree_testcase.userdata = {"model":data,"type": "variable"}

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
        _tree_keyword.userdata = {"model":data,"type": "keyword"}

        parent.add_child(_tree_keyword)

    def load_resources(self,data,parent):

        _labels = [
                    data.name,
                  ]

        _tree_resource = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                parent=parent)

        _tree_resource.icon     = "26b41084d7c558d94b50f5e1c40cdfd362f05478"
        _tree_resource.userdata = {"model":data,"type": "resource"}

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
        _tree_library.userdata = {"model":data,"type": "library"}

        parent.add_child(_tree_library)

    def load_external_resources(self,data,parent):

        _labels = ["External Resources"]

        _tree_ext_resources = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                parent=parent)

        _tree_ext_resources.icon     = "616b77c9b4e3020bee662e34c6feb5e8ddcd2b7d"
        _tree_ext_resources.userdata = {"model":None,"type":None}

        parent.add_child(_tree_ext_resources)

        for _resource in data:

            self.load_resources(_resource,_tree_ext_resources)

    def load_external_libraries(self,data,parent):

        _labels = ["External Libraries"]

        _tree_ext_libraries = SCR_WDG_Tree_Item(
                                                data=_labels,
                                                parent=parent)

        _tree_ext_libraries.icon     = "66a73259d66004e2b9c7180030bc347836ddcb82"
        _tree_ext_libraries.userdata = {"model":None,"type":None}

        parent.add_child(_tree_ext_libraries)

        for _resource in data:

            self.load_libraries(_resource,_tree_ext_libraries)

    def find_items_by_type(self,text,datatype):

        _items = []

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

    def __init__(self, config, search_clbk):

        SCR_WDG_Tree.__init__(
                                self,
                                config=config, 
                                search_clbk=search_clbk,
                                with_metadata=True,
                                model_class=SCR_WDG_TestTree_Model)

    def find_items_by_type(self,text,datatype):

        return self.custom_model.find_items_by_type(text,datatype)

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

        self.setStyleSheet('border: 1px solid #ffffff;')      
            
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
                    {"All"       : "all"       },
                    {"Test Suite": "testsuite" },
                    {"Test Case" : "testcase"  },
                    {"Keyword"   : "keyword"   },
                    {"Variable"  : "variable"  },
                    {"Folder"    : "testfolder"},
                    {"Resource"  : "resource"  },
                    {"Library"   : "library"   },
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

        #Animation
        self._animation = QPropertyAnimation(self,b"geometry")
        self._animation.setTargetObject(self)
        self._animation.setDuration(150)
        self._animation.setEasingCurve(QEasingCurve.Linear)           

    def selection_change(self):

        self.selection_type = self._selection.get_item_data(self._selection.currentText())

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