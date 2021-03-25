
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

    def __init__(self,config,icon_normal,icon_hover,tooltip,callback):

        QPushButton.__init__(self)

        self.config = config

        _css  = """
            border: 0px solid gray;
            background-color: %s;
        """  % (config.get_theme_background(),)

        self.setStyleSheet(_css)

        self.setIcon(SCR_GetIcon(icon_normal))
        self.setIconSize(QSize(30,30))

        self.icon_normal = icon_normal
        self.icon_hover  = icon_hover

        self.clicked.connect(callback)

        self.setToolTip(tooltip)

    def enterEvent(self,event):

        self.setIcon(SCR_GetIcon(self.icon_hover))

    def leaveEvent(self,event):

        self.setIcon(SCR_GetIcon(self.icon_normal)) 

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
        self.setWindowIcon(SWTW_GetIcon('d0f2525e4ec3b4d25285169ce8b0db1a4bb587cb'))
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