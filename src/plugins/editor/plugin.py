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
from control.control        import SCR_Control_Keyword
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

        self.table.setWordWrap(True)

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

        #only test case and keyword populate the editor table
        if type(data) in [SCR_Control_TestCase,SCR_Control_Keyword]:

            #empty entire table
            self.table.clear()

            #populate table with new controller
            self.table.populate(data)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_EditorGrid_Item(object):

    def __init__(self,config,data,row,column,empty):

        self.config           = config
        self.item_data        = data
        self.item_row         = row
        self.item_column      = column
        self.tooltip          = None
        self.empty            = empty
        self.background_color = config.get_theme_color_background()
        self.foreground_color = config.get_theme_color_foreground()

    def validate(self):
        """
        Method will check if the table item RF syntax is correct
        It will chose the appropriate color depending on the validity of the syntax
        """

        if self.empty == False:

            self.foreground_color = self.config.get_theme_color_keyword_valid()
        else:
            self.foreground_color = self.config.get_theme_color_foreground()

    def clear(self):
        """
        Empty the table item of all data
        """

        self.item_data        = None
        self.item_row         = -1
        self.item_column      = -1
        self.tooltip          = None
        self.empty            = True

    def get_text(self):
        """
        Get the text held by this table cell item
        If the table cell item is empty no text is returned
        """

        _text = ""

        if self.empty == False:

            _text = self.item_data.model.get_statement_text_by_index(self.item_row)[self.item_column]

        return _text

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

        self.items = SCR_Base_List()

        #the table received data will be a scrib controller
        self.data = data

        _max_rows    = self.rowCount(None) + 1
        _max_columns = self.columnCount(None) + 1
        _statements  = self.data.model.get_statements()

        #number of rows is equal to the number of statements (usefull) in the model
        for _row in range(_max_rows):

            _list_cells     = SCR_Base_List()

            if _row < len(_statements):

                _statement_size = self.data.model.get_statement_size(_statements[_row])
            else:
                _statement_size = 0

            #number of columns is the numbers of cells of the largest statement plus one (for design)
            for _column in range(_max_columns):

                #create a new table item for each statement and each cell
                _item = SCR_WDG_EditorGrid_Item(
                                                    config=self.config, 
                                                    data=self.data, 
                                                    row=_row,
                                                    column=_column,
                                                    empty=_column > (_statement_size - 1))

                _item.validate()

                _list_cells.add(_item)

            self.items.add(_list_cells)

    def rowCount(self, index):
        """
        Method called by QTableView widget to know how many roes to create
        """

        #number of row is the number of statements minus the last one (EOF)
        #added one more row for visual reasons and editing
        return self.data.model.get_nr_of_statements() + 1

    def columnCount(self, index):
        """
        Method called by QTableView widget to know how many roes to create
        """

        #number of columns is the maximum number of cells used by any statement
        #added one more column vor visual reasons and editing
        return self.data.model.get_max_statement_size() + 1

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

        _item.validate()

        #this is not ok: should be inserted not added
        self.items.add(_item)

        #notify QAbstractItemModel that we are done inserting rows in the model
        self.endInsertRows()

        #create the QModelIndex object
        _index = self.index(row, 0, _item)

        return _index
        
    def data(self, index, role):
        """
        Method called by QTableView when data about a table index is needed
        Role defines what type of data is requested
        """

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
                _data = _item.item_data

            elif role == Qt.ItemDataRole.BackgroundRole:

                _item = index.internalPointer()
                _data = QColor(_item.background_color)

            elif role == Qt.ItemDataRole.ForegroundRole:

                _item = index.internalPointer()
                _data = QColor(_item.foreground_color)

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
        """
        Table indexes do not have parent
        Return Nothing
        """

        _parent = QModelIndex()

        return _parent

    def clear(self):

        self.beginResetModel()

        for _row in self.items:

            for _item in _row:

                _item.clear()

        self.endResetModel()
