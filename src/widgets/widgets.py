
from PyQt5.QtCore          import *
from PyQt5.QtGui           import *
from PyQt5.QtWidgets       import * 
from icons.icons           import SCR_GetIcon

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

    def __init__(self,icon_normal,icon_hover,callback):

        QPushButton.__init__(self)

        self.setStyleSheet('''QPushButton { 
                                padding: 0px; 
                                border: 0; 
                                border-radius: 0px; 
                                outline: 0px; 
                            }''')

        self.setIcon(SCR_GetIcon(icon_normal))
        self.setIconSize(QSize(30,30))

        self.icon_normal = icon_normal
        self.icon_hover  = icon_hover

    def enterEvent(self,event):

        self.setIcon(SCR_GetIcon(self.icon_hover))

    def leaveEvent(self,event):

        self.setIcon(SCR_GetIcon(self.icon_normal)) 

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_ToolBar(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        self.wdgs = {}

    def add_button(self,name,icon_normal,icon_hover,callback):

        _button = SCR_WDG_Button(icon_normal,icon_hover,callback)

        self.wdgs.update({name:_button})

    def draw(self):

        self.ly = QHBoxLayout()

        for _name in self.wdgs:

            self.ly.addWidget(self.wdgs[_name])

        self.setLayout(self.ly)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_WDG_PlainTextEdit(QPlainTextEdit):

    def __init__(self):

        QPlainTextEdit.__init__(self)

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_Console(QWidget):


    def __init__(self):

        QWidget.__init__(self)

        self.__create_gui()

    def __create_gui(self):

        self.text = SCR_WDG_PlainTextEdit()
        self.text.setStyleSheet('background: #080008; color:#999999; ')
        self.text.setFont(QFont("Courier", 9));

        #set console to read-only
        self.text.setReadOnly(True)      
        self.text.setContextMenuPolicy(Qt.NoContextMenu)      

        self.input = QLineEdit()
        self.input.setStyleSheet('background: gray; color: white;')

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.text)
        self.setLayout(vertical_layout)

    def write(self,txt,level):

        pass
