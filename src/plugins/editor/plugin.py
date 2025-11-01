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
                                    search_clbk=None,
                                    model_class=SCR_WDG_EditorGrid_Model)

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

            print(data.model.get_nr_of_statements())
            print(data.model.get_max_statement_size())

            #self.table.populate(data)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_EditorGrid_Item(object):

    def __init__(self,config,data,data_index):

        #the controler entire model
        self.user_data        = data

        #the index of the statement held by this table index
        self.user_data_index  = data_index

        self.tooltip          = None
        self.background_color = config.get_theme_background()

    def column_count(self):

        #get the number of operands in the statement
        return self.user_data.get_statement_size[self.user_data_index]

    def data(self, column):

        _data = None

        try:
            _data = self.item_data[column]

        except IndexError:

            _data =  None

        return _data

    def parent(self):

        return None

    def row(self):

        return self.index(self)

    def clear(self):

        self.tooltip     = None
        self.userdata    = None

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

    def load(self,data):

        #the table received data will be a scrib controller
        #store it...it will be needed
        self.data = data

    def rowCount(self, index):

        return index.internalPointer().data.model.get_nr_of_statements()

    def columnCount(self, index):

        return index.internalPointer().data.model.get_nr_of_statements()

        return _count

    def insertRow(self,row):

        self.beginInsertRows(parent,row,row)

        _parent_item = parent.internalPointer()

        _new_item = SCR_WDG_Table_Item(
                                        data=[text],
                                        data_index=row,
                                        config=self.config,
                                        parent=_parent_item)

        _parent_item.add_child(_new_item)

        self.endInsertRows()

        return self.index(_parent_item.child_count() - 1,0,parent)
        
    def data(self, index, role):

        _data = None

        if index.isValid():

            if role == Qt.ItemDataRole.DisplayRole:

                _item = index.internalPointer()
                _data = _item.data(index.column())
            else:
                if role == Qt.ItemDataRole.DecorationRole:

                    _item = index.internalPointer()

                else:
                    if role == Qt.ItemDataRole.ToolTipRole:

                        if index.column() == 0:

                            _item = index.internalPointer()
                            _data = _item.tooltip

                    else:
                        if role == Qt.ItemDataRole.UserRole:

                            _item = index.internalPointer()
                            _data = _item.userdata

                        else:
                            if role == Qt.ItemDataRole.BackgroundRole:

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

    def headerData(self, section, orientation, role):

        _hader_data = None

        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:

            #TO DO: actual header infor later
            _hader_data = None

        return _hader_data

    def index(self, row, column, parent):

        _index = QModelIndex()

        if self.hasIndex(row, column, parent):

            if not parent.isValid():
                _parent_item = self.root
            else:
                _parent_item = parent.internalPointer()

            _child_item = _parent_item.child(row)

            if _child_item:

                _index = self.createIndex(row, column, _child_item)

        return _index

    def parent(self, index):

        _parent = QModelIndex()

        if index.isValid():

            _child_item  = index.internalPointer()
            _parent_item = _child_item.parent()

            if _parent_item != self.root:

                if _parent_item != None:

                    _parent = self.createIndex(_parent_item.row(), 0, _parent_item)

        return _parent

    def clear(self):

        self.beginResetModel()
        self.endResetModel()

    def find_items(self,text,column):

        _items = []

        for _row in range(self.root.child_count()):

            _items += self.find(
                                _row,
                                column,
                                text,
                                QModelIndex())

        return _items

    def find(self,row,column,text,parent):

        _finds = []
        _index = self.index(row, column, parent)
        _data  = _index.data(Qt.ItemDataRole.DisplayRole)

        if text.lower() in _data.lower():

            _finds.append(_index)

        _index_root = self.index(row, 0, parent)

        for _child_row in range(self.rowCount(_index_root)):

            _finds += self.find(
                                _child_row, 
                                column, 
                                text, 
                                _index_root)

        return _finds