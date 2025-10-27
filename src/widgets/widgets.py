"""
File contains all UI base widgets that will be used.
It is not allowed to use Qt Widgets directly in Srib code.
Instead a Qt widget must be wrapper in a class and then used.
This will ensure easy global changes and some degree of isolation 
from future changes in the Qt library.
The theme colors can easilly be applied from the wrapper widget.
"""

from PyQt6.QtCore          import *
from PyQt6.QtGui           import *
from PyQt6.QtWidgets       import * 
from icons.icons           import SCR_GetIcon
from abc                   import abstractmethod



"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_ProgressBar(QProgressBar):

    def __init__(self,config):

        self.config = config

        QProgressBar.__init__(self)

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_StatusBar(QStatusBar):

    def __init__(self,config):

        self.config = config

        QStatusBar.__init__(self)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_MenuBar(QMenuBar):

    def __init__(self,config,*args):

        QMenuBar.__init__(self,*args)

        self.config = config

        _css  = """
                    QMenuBar::item 
                    {
                        background-color: %s;
                        color: %s;
                        padding: 4px 20px 4px 20px;
                    }

                    QMenuBar::item:selected 
                    {
                        background-color: %s; 
                        color: %s;
                    }

                    QMenuBar QAbstractItemView::item
                    {

                        border-width: 3px;
                        border-style: solid;
                        border-color: #E74C3C; 
                        border-radius: 5px;
                    }

                """

        _css = _css % (
                            self.config.get_theme_background(),
                            self.config.get_theme_foreground(),
                            self.config.get_theme_sel_background(),
                            self.config.get_theme_sel_foreground())

        self.setStyleSheet(_css)

    def add_menu(self,parent,name):

        _menu = parent.addMenu(name)

        _css  = """
                    QMenu::item {
                        background-color: %s;
                        color: %s;
                        padding: 4px 20px 4px 20px; 
                    }

                    QMenu::item:selected {
                        background-color: %s; 
                        color: %s;
                    }
                """

        _css = _css % (
                            self.config.get_theme_background(),
                            self.config.get_theme_foreground(),
                            self.config.get_theme_sel_background(),
                            self.config.get_theme_sel_foreground())

        _menu.setStyleSheet(_css)

        return _menu

    def add_action(self,parent,text,icon,shortcut,callback):

        _action = QAction(parent)
        _action.setText(text)
        _action.setIcon(SCR_GetIcon(icon))

        if shortcut != None:
            _action.setShortcut(shortcut)

        _action.triggered.connect(callback)
        parent.addAction(_action)

        return _action

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_ToolButton(QToolButton):

    def __init__(self,config):

        QToolButton.__init__(self)

        self.config = config

        _css  = """
        background-color: %s;
        color: %s; 
        """ % (self.config.get_theme_background(),self.config.get_theme_foreground())

        self.setStyleSheet(_css)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_LineEdit(QLineEdit):

    def __init__(self,config):

        QLineEdit.__init__(self)

        self.config = config

        _css  = """
        background-color: %s;
        color: %s; 
        """ % (self.config.get_theme_background(),self.config.get_theme_foreground())

        self.setStyleSheet(_css)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_Widget(QWidget):

    def __init__(self,*args):

        QWidget.__init__(self,*args)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_DockWidget(QDockWidget):

    def __init__(self,config):

        QDockWidget.__init__(self)


        self.config = config

        _css  = """
        background-color: %s;
        color: %s; 
        """ % (self.config.get_theme_background(),self.config.get_theme_foreground())

        self.setStyleSheet(_css)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_Button(QPushButton):

    def __init__(self,config,icon_normal,icon_hover,tooltip,callback):

        QPushButton.__init__(self)

        self.icon_size = 25

        self.config = config

        _css  = """
            border: 0px solid gray;
            background-color: %s;
        """  % (self.config.get_theme_background(),)

        self.setStyleSheet(_css)

        self.setIcon(SCR_GetIcon(icon_normal))
        self.setIconSize(QSize(self.icon_size,self.icon_size))

        self.icon_normal = icon_normal
        self.icon_hover  = icon_hover

        self.clicked.connect(callback)

        self.setToolTip(tooltip)

    def enterEvent(self,event):

        self.setIcon(SCR_GetIcon(self.icon_hover))
        self.setIconSize(QSize(self.icon_size,self.icon_size))

    def leaveEvent(self,event):

        self.setIcon(SCR_GetIcon(self.icon_normal)) 
        self.setIconSize(QSize(self.icon_size,self.icon_size))

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_ToolBar(QWidget):

    def __init__(self,config):

        QWidget.__init__(self)

        self.wdgs   = {}
        self.config = config

    def add_button(self,name,icon_normal,icon_hover,tooltip,callback):

        _button = SCR_WDG_Button(self.config,icon_normal,icon_hover,tooltip,callback)

        self.wdgs.update({name:_button})

    def draw(self):

        self.ly = QHBoxLayout()

        for _name in self.wdgs:

            self.ly.addWidget(self.wdgs[_name])

        self.ly.addWidget(QSplitter())        

        self.setLayout(self.ly)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_PlainTextEdit(QPlainTextEdit):

    def __init__(self):

        QPlainTextEdit.__init__(self)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_PopUp(QMessageBox):

    def __init__(self,title,txt,msgtype="information"):

        QMessageBox.__init__(self)

        self.txt     = txt
        self.title   = title
        self.msgtype = msgtype

        self.draw_gui()

        self.exec_()

    def draw_gui(self):

        self.setWindowTitle(self.title)
        self.setWindowIcon(SCR_GetIcon('08e0c30ab7f9c6d43c70165c4ae42460d460c0aa'))
        self.resize(400,40)
        self.setFixedSize(400,40)
        self.setStyleSheet("background-color: #ffffff")
        self.setText(self.txt)
        self.setWindowModality(Qt.ApplicationModal)

        if self.msgtype == "question":
            self.setIcon(QMessageBox.Question)
            self.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
        else:
            if self.msgtype == "information":
                self.setIcon(QMessageBox.Information)
            else:
                if self.msgtype == "warning":
                    self.setIcon(QMessageBox.Warning)
                else:
                    if self.msgtype == "critical":
                        self.setIcon(QMessageBox.Critical)
                    else:
                        self.setIcon(QMessageBox.NoIcon)

        self.setStandardButtons(QMessageBox.Ok)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_Tree_Item(object):

    def __init__(self, data, config, parent=None):

        self.parent_item      = parent
        self.item_data        = data
        self.child_items      = []
        self.icon             = None
        self.tooltip          = None
        self.userdata         = None
        self.background_color = config.get_theme_background()

    def add_child(self, item):

        self.child_items.append(item)

    def child(self, row):

        return self.child_items[row]

    def child_count(self):

        return len(self.child_items)

    def column_count(self):

        return len(self.item_data)

    def data(self, column):

        _data = None

        try:
            _data = self.item_data[column]

        except IndexError:

            _data =  None

        return _data

    def parent(self):

        return self.parent_item

    def row(self):
        
        if self.parent_item:

            return self.parent_item.child_items.index(self)

        return 0

    def clear(self):

        self.child_items = []
        self.icon        = None
        self.tooltip     = None
        self.userdata    = None

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_Tree_Model(QAbstractItemModel):
    # this class cannot be used as is
    # it must be inherited and certain methods reimplemented

    def __init__(self, config, parent=None):

        QAbstractItemModel.__init__(self)

        self.root = None

        self.config = config

    @abstractmethod
    def load(self, data, parent):

        #to be implemented in child class
        pass

    def columnCount(self, parent):

        if parent.isValid():

            return parent.internalPointer().column_count()
        else:
            return self.root.column_count()

    def data(self, index, role):

        _data = None

        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole:

                _item = index.internalPointer()
                _data = _item.data(index.column())
            else:
                if role == Qt.ItemDataRole.DecorationRole:
                    _item = index.internalPointer()
                    if _item.icon != None:
                        if type(_item.icon) != list:
                            if index.column() == 0:
                                _data = SCR_GetIcon(_item.icon,size="small")
                        else:
                            if _item.icon[index.column()] != None:
                                _data = SCR_GetIcon(_item.icon[index.column()],size="small")
                            else:
                                _data = None
                    else:
                        _data = None
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

            _hader_data = self.root.data(section)

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

    def rowCount(self, parent):

        _count = 0

        if parent.column() > 0:

            _count = 0
        else:

            if not parent.isValid():
                _parent_item = self.root
            else:
                _parent_item = parent.internalPointer()

            _count = _parent_item.child_count()

        return _count

    def clear(self):

        if self.root != None:

            self.beginResetModel()
            self.root.clear()
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

    def insertRow(self,row,parent,text):

        self.beginInsertRows(parent,row,row)

        _parent_item = parent.internalPointer()

        _new_item = SCR_WDG_Tree_Item(
                                        data=[text],
                                        config=self.config,
                                        parent=_parent_item)

        _parent_item.add_child(_new_item)

        self.endInsertRows()

        return self.index(_parent_item.child_count() - 1,0,parent)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_Tree(QTreeView):
    
    def __init__(self, config, search_clbk, with_metadata=True, model_class=SCR_WDG_Tree_Model):

        QTreeView.__init__(self)

        self.config = config

        _css  = ""
        _css += "background-color: {};".format(self.config.get_theme_background(),)
        _css += "color: {};".format(self.config.get_theme_foreground(),)  
        _css += "selection-color: {};".format(self.config.get_theme_sel_foreground(),) 
        _css += "selection-background-color: {};".format(self.config.get_theme_sel_background(),) 
        _css += "font-family: Arial;"
        _css += "font-size: 9pt;"
        _css += "border: 1px solid #707070;"

        self.setStyleSheet(_css)

        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.search_clbk   = search_clbk
        self.root          = SCR_WDG_Tree_Item(
                                                data=[""],                                                    
                                                config=self.config,
                                                parent=None,)
        self.with_metadata = with_metadata
        self.custom_model  = model_class(config=self.config, parent=self)

    def expandChildren(self,item):

        if item.isValid():

            _count = item.model().rowCount(item)
            
            for _index in range(_count):

                _child = item.child(_index, 0)

                self.expandChildren(_child);            

                self.expand(item)            

    def collapseChildren(self,item):

        if item.isValid():

            _count = item.model().rowCount(item)
            
            for _index in range(_count):

                _child = item.child(_index, 0)

                self.collapseChildren(_child);            

                self.collapse(item)  

    def populate(self, data, header):

        self.root = SCR_WDG_Tree_Item(
                                            data=header,
                                            config=self.config,
                                            parent=None)

        self.custom_model.root = self.root
        self.custom_model.load(data, self.root) 

        self.setModel(self.custom_model)  

    def clear(self):

        self.custom_model.clear()
        
    def get_user_data(self,item):

        if self.with_metadata:
            _serial_data = item.data(Qt.ItemDataRole.UserRole)
        else:
            _serial_data = None

        return _serial_data

    def keyPressEvent(self, event):

        _find_shortcut = (event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_F)  

        if _find_shortcut:

            if self.search_clbk != None:

                self.search_clbk()

        QWidget.keyPressEvent(self,event) 
 
    def find_items(self,text,column):

        return self.custom_model.find_items(text,column)

    def scrollToItem(self,item):

        self.scrollTo(item)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_Selection(QComboBox):

    def __init__(self,config):

        QComboBox.__init__(self)

        self.config = config

        _css  = """  background-color: %s;
                     color: %s;  
                     border-radius: 3px;
                     font-size: 9pt;
                     font-family: Arial;

                     """ % (self.config.get_theme_background(), self.config.get_theme_foreground())

        self.setStyleSheet(_css)
        self.editTextChanged.connect(self.textChangedHandler)
        self.setEditable(True)
        self.data = []
        self._model_items = []


    def __create_completer(self):

        self.completer = QCompleter()

        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)

        self.setCompleter(self.completer)        

        self.model = QStringListModel()

        self.completer.setModel(self.model)        

        self._model_items = [list(_item.keys())[0] for _item in self.data]

        self.model.setStringList(self._model_items)

        self.completer.setModelSorting(QCompleter.ModelSorting.CaseInsensitivelySortedModel)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setCompletionRole(Qt.ItemDataRole.DisplayRole)

    def populate(self,data,defaultvalue=None):

        self.data = data

        self.clear()
        for _item in self.data:

            self.addItem(list(_item.keys())[0])

        self.__create_completer()

        if defaultvalue == None:
            self.setCurrentIndex(0)
        else:
            _index     = 0
            _the_index = 0
            for _item in self.data: 
                if defaultvalue == _item[list(_item.keys())[0]]:
                    _the_index = _index

                _index += 1

            self.setCurrentIndex(_the_index)

    def get_item_data(self,text):

        _data = ""

        for _index in range(len(self.data)):

            if list(self.data[_index].keys())[0] == text:

                _data = self.data[_index][list(self.data[_index].keys())[0]]
        
        return _data

    def textChangedHandler(self, text):

        if self._model_items:

            if str(text) in self._model_items or not len(text):
                self.setStyleSheet("background-color: %s; color: %s;  " % (self.config.get_theme_background(),self.config.get_theme_foreground()))
            else: 
                self.setStyleSheet("background-color: #ffcccc; color: %s;  " % (self.config.get_theme_foreground(),))

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_Label(QLabel):

    def __init__(self,config,txt=""):

        QLabel.__init__(self,txt)

        self.config = config

        _css  = """
        background-color: %s;
        color: %s; 
        border: 0px solid gray;
        font-family: Arial;

        """ % (self.config.get_theme_background(),self.config.get_theme_foreground())

        self.setStyleSheet(_css)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_ActionBar(QWidget):

    def __init__(self,app,parent,config):

        QWidget.__init__(self,parent)
  
        self.app            = app
        self.config         = config
        self.text_limit     = 50
        self.text_wdg_width = 300
        self.is_canceled    = False
    
        self.draw_text()
        self.draw_progress()
        self.draw_cancel_button()

        self.setFixedHeight(35)
        self.setFixedHeight(35)       

        self.ly  = QHBoxLayout()
        self.ly.addWidget(self.wdg_txt) 
        self.ly.addWidget(self.wdg_progress)
        self.ly.addWidget(self.cancel_bt)
        self.setLayout(self.ly)

        self.setStyleSheet("border: 0px solid white; margin: 0px;")

        self.stop()

    def draw_text(self):

        self.wdg_txt = SCR_WDG_Label(self.config,"")

        _font = QFont()
        _font.setPointSize(8)

        self.wdg_txt.setFont(_font)
        self.wdg_txt.setFixedWidth(self.text_wdg_width)
        self.wdg_txt.setStyleSheet("border: 1px solid gray; border-radius: 4px; color: %s" % (self.config.get_theme_foreground(),))

    def draw_progress(self):

        self.wdg_progress   = SCR_WDG_ProgressBar(self)

        self.wdg_progress.setFixedHeight(8)
        self.wdg_progress.setTextVisible(False)
        self.wdg_progress.setMinimum(0)
        self.wdg_progress.setMaximum(100)

    def draw_cancel_button(self):

        self.cancel_bt = SCR_WDG_Button(
                                            self.config,
                                            "08fbdd84bc6f62fe1b927b9115596ab50cbca623",
                                            "08fbdd84bc6f62fe1b927b9115596ab50cbca623",
                                            "Cancel",
                                            self.cancel)
        self.cancel_bt.setFixedWidth(35)

        self.cancel_bt.hide()

        self.wdg_progress.setStyleSheet("border: 1px solid gray; border-radius: 4px;")

    def start(self,withload=False,withcancel=False):

        self.is_canceled   = False

        if withcancel:
            self.cancel_bt.show()
        else:
            self.cancel_bt.hide()

        self.setVisible(True)

        self.message("")

        self.progress(0)  

        self.wdg_progress.setVisible(withload)

        self.app.processEvents()

    def stop(self):

        self.message("")
        self.progress(0)
        self.setVisible(False)

    def progress(self,value):

        self.wdg_progress.setValue(value)
        self.wdg_progress.update()
        self.app.processEvents()

    def message(self,text):

        if len(text) > self.text_limit:

            text = "{}...".format(text[:self.text_limit])

        self.wdg_txt.setText(text)
        self.app.processEvents()

    def cancel(self,state):

        self.is_canceled = True

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_RadioButton(QRadioButton):

    def __init__(self,config,label):

        QRadioButton.__init__(self,label)

        _css  = """
        background-color: %s;
        color: %s; 
        """ % (self.config.get_theme_background(),self.config.get_theme_foreground())

        self.setStyleSheet(_css)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_CheckBox(QCheckBox):

    def __init__(self,config,label):

        QCheckBox.__init__(self,label)

        _css = """
        font-family: Arial;
        background-color: %s;
        color: %s; 
        """ % (self.config.get_theme_background(),self.config.get_theme_foreground())

        self.setStyleSheet(_css)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_Tab(QTabWidget):

    def __init__(self,config):

        QTabWidget.__init__(self)

        self.config = config

        _css  = """
        QTabWidget::pane { 
                            border: 1px solid #707070;
                            border-radius: 3px;
                         }

        QTabBar::tab {
                    border: 1px solid #707070;
                    border-bottom-color: #bfc0c1;
                    min-width: 55ex;
                    font-family: Arial;
                    padding: 2px;
                    border-radius: 3px;
                    color: #494949
                }

        QTabBar::tab:selected {
            border-color: gray;
            border-bottom-color: #707070; 
            background-color: #c1c1c1;
            border-radius: 3px;
            color:%s

        }

        QTabBar::tab:!selected {
            margin-top: 4px; /* make non-selected tabs look smaller */
            color:%s
        }

        """ % (self.config.get_theme_foreground(),self.config.get_theme_foreground())

        self.setStyleSheet(_css)

    def add_tab(self,label):

        _widget = SCR_WDG_Widget()

        self.addTab(_widget,label)

        return _widget