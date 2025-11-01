"""
File contains all UI widgets regarding the Test Case and Keyword editor grid
"""

from PyQt6.QtCore           import *
from PyQt6.QtGui            import *
from PyQt6.QtWidgets        import * 
from widgets.widgets        import SCR_WDG_Widget
from widgets.widgets        import SCR_WDG_Table
from widgets.plugin_manager import SCR_Plugin
from control.control        import SCR_Control_TestCase
from model.model            import SCR_Base_List

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
        """
        Function will be called by plugin manager when the plugin must be shown
        """

        self.draw_gui()

        self.subscribe()

    def unload(self):
        """
        Function will be called by plugin manager when the plugin must be hidden
        """

        pass

    def draw_gui(self):
        """
        Create all widgets and objects needed to draw the plugin UI
        """

        self.table = SCR_WDG_Table(
                                    config=self.config, 
                                    model_class=SCR_WDG_EditorGrid_Model)

        self.ly = QVBoxLayout()

        self.ly.addWidget(self.table)    

        self.setLayout(self.ly)

    def subscribe(self):
        """
        Subscribe to all needed Scrib messages
        """

        self.messenger.subscribe("TestTreeSelectionChange", self.on_test_tree_selection_change)

    def on_test_tree_selection_change(self,data):
        """
        Function called by scrib when the user selects a new item in the test tree
        """

        if type(data) == SCR_Control_TestCase:

            self.table.populate(data)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_EditorGrid_Item(object):

    def __init__(self,config,data,row,column):

        self.item_data        = data
        self.item_row         = row
        self.item_column      = column
        self.tooltip          = None
        self.background_color = config.get_theme_background()

    def clear(self):
        """
        Empty the table item of all data
        """

        self.item_data   = None
        self.tooltip     = None

    def get_text(self):

        _text_cells = self.item_data.model.get_statement_text_by_index(self.item_row)

        return _text_cells[self.item_column]

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_EditorGrid_Model(QAbstractItemModel):
    """
    Model class used by Table widget to store and load data
    """

    def __init__(self, config, parent):

        QAbstractItemModel.__init__(self)

        self.parent  = parent
        self.config  = config
        self.data    = None
        self.items   = SCR_Base_List()

    def load(self,data):
        """
        Load all data from a scrib controller in the table view
        """

        #the table received data will be a scrib controller
        self.data = data

        _row = 0

        for _statement in self.data.model.get_statements():

            _list_operands = SCR_Base_List()

            for _column in range(self.data.model.get_statement_size(_statement)):

                _item = SCR_WDG_EditorGrid_Item(
                                                    config=self.config, 
                                                    data=self.data, 
                                                    row=_row,
                                                    column=_column)

                _list_operands.add(_item)

            _row += 1

            self.items.add(_list_operands)

    def rowCount(self, index):

        return 2

    def columnCount(self, index):

        return 3

    def insertRow(self,row,data,data_index):
        """
        Insert a new row in the model
        """

        #notify QAbstractItemModel that we are about to insert rows in the model
        self.beginInsertRows(parent,row,row)

        #create a new item in the table
        _item = SCR_WDG_EditorGrid_Item(
                                            config=self.config, 
                                            data=self.data, 
                                            data_index=_statement_index)

        #this is not ok: should be inserted not added
        self.items.add(_item)

        #notify QAbstractItemModel that we are done inserting rows in the model
        self.endInsertRows()

        #create the QModelIndex object
        _index = self.index(row, 0, _item)

        return _index
        
    def data(self, index, role):

        _data = None

        if index.isValid():

            if role == Qt.ItemDataRole.DisplayRole:

                _item = index.internalPointer()
                _data = _item.get_text()

            elif role == Qt.ItemDataRole.DecorationRole:

                _item = index.internalPointer()

            elif role == Qt.ItemDataRole.ToolTipRole:

                _item = index.internalPointer()
                _data = _item.tooltip

            elif role == Qt.ItemDataRole.UserRole:

                _item = index.internalPointer()
                _data = [_item.item_data,_item.item_data_index]

            elif role == Qt.ItemDataRole.BackgroundRole:

                _item = index.internalPointer()
                _data = _item.background_color

            else:
                _data = None
        else:
            _data = None

        return _data

    def flags(self, index):

        _flags = Qt.ItemFlag.NoItemFlags

        if index.isValid():

            _flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable

        return _flags

    def index(self, row, column, item):

        _index = self.createIndex(row, column, self.items[row][column])

        return _index

    def parent(self, index):

        _parent = QModelIndex()

        return _parent

    def clear(self):

        self.beginResetModel()

        self.endResetModel()
