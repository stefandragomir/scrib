
from PyQt5.QtCore          import *
from PyQt5.QtGui           import *
from PyQt5.QtWidgets       import * 
from icons.icons           import SCR_GetIcon
from abc                   import abstractmethod

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_DockWidget(QDockWidget):

    def __init__(self):

        QDockWidget.__init__(self)

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

    def __init__(self, data, parent=None):

        self.parent_item      = parent
        self.item_data        = data
        self.child_items      = []
        self.icon             = None
        self.tooltip          = None
        self.userdata         = None
        self.background_color = QColor("#ffffff")

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

    def __init__(self, parent=None):

        QAbstractItemModel.__init__(self)

        self.root = None

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
            if role == Qt.DisplayRole:

                _item = index.internalPointer()
                _data = _item.data(index.column())
            else:
                if role == Qt.DecorationRole:
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
                    if role == Qt.ToolTipRole:
                        if index.column() == 0:
                            _item = index.internalPointer()
                            _data = _item.tooltip
                    else:
                        if role == Qt.UserRole:
                            _item = index.internalPointer()
                            _data = _item.userdata
                        else:
                            if role == Qt.BackgroundRole:
                                _item = index.internalPointer()
                                _data = _item.background_color
                            else:
                                _data = None
        else:
            _data = None

        return _data

    def flags(self, index):

        _flags = Qt.NoItemFlags

        if index.isValid():

            _flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable

        return _flags

    def headerData(self, section, orientation, role):

        _hader_data = None

        if orientation == Qt.Horizontal and role == Qt.DisplayRole:

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

    def findItems(self,text,column):

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
        _data  = _index.data(Qt.DisplayRole)

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

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_Tree(QTreeView):
    
    def __init__(self, config, usefind=False, with_metadata=True, model_class=SCR_WDG_Tree_Model):

        QTreeView.__init__(self)

        self.config = config

        _css  = ""
        _css += "background-color: %s;" % (self.config.get_theme_background(),)
        _css += "color: %s;" % (self.config.get_theme_foreground(),)  
        _css += "selection-color: #000000;"
        _css += "selection-background-color: #c2d2ed;"
        _css += "font-family: Arial;"
        _css += "font-size: 9pt;"
        _css += "border: 1px solid #707070;"

        self.setStyleSheet(_css)

        self.setSelectionMode(QAbstractItemView.SingleSelection)

        self.usefind       = usefind
        self.root          =  SCR_WDG_Tree_Item(data=[""],parent=None)
        self.with_metadata = with_metadata
        self.custom_model  = model_class(parent=self)

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
                                            parent=None)

        self.custom_model.root = self.root
        self.custom_model.load(data, self.root) 

        self.setModel(self.custom_model)  

    def clear(self):

        self.custom_model.clear()
        
    def get_user_data(self,item):

        if self.with_metadata:
            _serial_data = item.data(Qt.UserRole)
        else:
            _serial_data = None

        return _serial_data

    def keyPressEvent(self, event):

        _find_shortcut = (event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_F)  

        if _find_shortcut:

            if self.usefind:

                self.search_tree()

        QWidget.keyPressEvent(self,event) 

    def search_tree(self):

        self.search = SCR_WDG_Tree_Find_Dialog( self)
        self.search.show()   

    def findItems(self,text,column):

        return self.custom_model.findItems(text,column)

    def scrollToItem(self,item):

        self.scrollTo(item)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_Tree_Find_Dialog(QWidget):

    def __init__(self,config,tree):

        QWidget.__init__(self,tree)

        self.config = config

        self._items          = []
        self._item_idx       = 0
        self._text_changed   = False
        self.tree            = tree
        self.selected_column = 0
           
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup )         
            
        #write line
        self.line = QLineEdit()
        self.line.setContextMenuPolicy(Qt.NoContextMenu)    
        self.line.setStyleSheet('border: 2px solid gray;')
        self.line.returnPressed.connect(self._find_next) 
        self.line.textEdited.connect(self._textedited)

        #find previous button
        self._find_prev_button = QToolButton()
        self._find_prev_button.setStyleSheet("background: transparent; border-radius: 0px")
        self._find_prev_button.setIcon(SCR_GetIcon('47d97a19678ecbc93257bfc890b71cc62f4ae908'))
        self._find_prev_button.clicked.connect(self._find_prev)                 

        #find next button
        self._find_next_button = QToolButton()
        self._find_next_button.setStyleSheet("background: transparent; border-radius: 0px")
        self._find_next_button.setIcon(SCR_GetIcon('85905e29412dc4ee1bca3b78beeca05a0ea1d14b'))
        self._find_next_button.clicked.connect(self._find_next)           

        #close button
        self._close_button = QToolButton()
        self._close_button.setStyleSheet("background: transparent; border-radius: 0px")
        self._close_button.setIcon(SCR_GetIcon('779d79bcda4833c45d97b063d0041af2e47265e4'))
        self._close_button.clicked.connect(self._close)

        #column selection
        self._selection = SCR_WDG_Selection(self.config)
        self._selection.setFixedWidth(150)
        self._selection.currentIndexChanged.connect(self.selection_change)
        _data = []
        if self.tree.custom_model.root != None:
            for _index in range(len(self.tree.custom_model.root.item_data)):
                _data.append({self.tree.custom_model.root.item_data[_index]:_index})
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
        
        QShortcut(QKeySequence(Qt.Key_Escape), self).activated.connect(self._close)           
        QShortcut(QKeySequence(Qt.CTRL + Qt.Key_F), self).activated.connect(self._close)    

        #Animation
        self._animation = QPropertyAnimation(self,b"geometry")
        self._animation.setTargetObject(self)
        self._animation.setDuration(150)
        self._animation.setEasingCurve(QEasingCurve.Linear)           

    def selection_change(self):

        self.selected_column = self._selection.currentText()

        self.selected_column = self._selection.get_item_data(self.selected_column)

    def showEvent(self, event): 

        _point = self.tree.mapToGlobal(QPoint(self.tree.geometry().x(),self.tree.geometry().y()))

        _x,_y = _point.x(),_point.y()
        
        self._animation.setStartValue( QRect(_x, _y + 200, self.width(), self.height()) )
        self._animation.setEndValue( QRect(_x, _y + 30, self.width(), self.height()) )
        self._animation.start() 
        
        self.line.setFocus()

    def _close(self):

        _point = self.tree.mapToGlobal(QPoint(self.tree.geometry().x(),self.tree.geometry().y()))

        _x,_y = _point.x(),_point.y()

        self._animation.setStartValue(QRect(_x, _y + 30, self.width(), self.height()))
        self._animation.setEndValue(QRect(_x, _y + 200, self.width(), self.height()))
        self._animation.start()
        self._animation.finished.connect(self.close)

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

                self._items = self.tree.findItems(self.word, self.selected_column)

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

                self._items = self.tree.findItems(self.word, self.selected_column)

            if self._item_idx < len(self._items) and self._item_idx >= 0:

                _item           = self._items[self._item_idx]   
                self._item_idx -= 1
            else:
                _item = None

            self.go_to_item(_item)   

    @property
    def word(self):

        return str(self.line.text())

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

        self.completer.setFilterMode(Qt.MatchContains)

        self.setCompleter(self.completer)        

        self.model = QStringListModel()

        self.completer.setModel(self.model)        

        self._model_items = [list(_item.keys())[0] for _item in self.data]

        self.model.setStringList(self._model_items)

        self.completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionRole(Qt.DisplayRole)

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
class SCR_WDG_StatusBar(QWidget):

    def __init__(self,app,parent,config):

        QWidget.__init__(self,parent)

        self.app          = app
        self.config       = config
        self.wdg_txt      = SCR_WDG_Label(self.config,"")
        self.wdg_progress = QProgressBar(self)
        self.wdg_progress.setFixedHeight(8)
        self.wdg_progress.setTextVisible(False)
        self.wdg_progress.setMinimum(0)
        self.wdg_progress.setMaximum(100)
        self.is_canceled  = False

        _font = QFont()
        _font.setPointSize(8)
        self.wdg_txt.setFont(_font)

        self.setFixedHeight(40)
        self.setFixedHeight(40)

        self.cancel_bt = SCR_WDG_Button(
                                            self.config,
                                            "08fbdd84bc6f62fe1b927b9115596ab50cbca623",
                                            "08fbdd84bc6f62fe1b927b9115596ab50cbca623",
                                            "Cancel",
                                            self.cancel)
        self.cancel_bt.setFixedWidth(40)


        self.ly  = QHBoxLayout()
        self.ly.addWidget(self.wdg_txt) 
        self.ly.addWidget(self.wdg_progress)
        self.ly.addWidget(self.cancel_bt)
        self.setLayout(self.ly)
        self.cancel_bt.hide()

        self.setStyleSheet("border: 0px solid white; margin: 0px;")

        self.wdg_txt.setStyleSheet("border: 1px solid gray; border-radius: 4px; color: %s" % (self.config.get_theme_foreground(),))
        self.wdg_progress.setStyleSheet("border: 1px solid gray; border-radius: 4px;")

        

        self.stop()

    def start(self,withload=False,withcancel=False):

        self.is_canceled   = False

        if withcancel:
            self.cancel_bt.show()
        else:
            self.cancel_bt.hide()

        self.setVisible(True)
        self.msg("")
        self.progress(0)        
        self.wdg_progress.setVisible(withload)
        self.app.processEvents()

    def stop(self):

        self.msg("")
        self.progress(0)
        self.setVisible(False)

    def progress(self,value):

        self.wdg_progress.setValue(value)
        self.wdg_progress.update()
        self.app.processEvents()

    def msg(self,msg):

        self.wdg_txt.setText(msg)
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

        _widget = QWidget()

        self.addTab(_widget,label)

        return _widget