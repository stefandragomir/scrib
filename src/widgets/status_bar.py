

from PyQt5.QtCore          import *
from PyQt5.QtGui           import *
from PyQt5.QtWidgets       import * 
from icons.icons           import SCR_GetIcon
from widgets.widgets       import SCR_WDG_Tab

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_Status_Bar(QStatusBar):

    def __init__(self,config):

        self.config = config

        QStatusBar .__init__(self)

        self.lbl = QLabel()

        self.addPermanentWidget(self.lbl)

    def message(self,msg):

        self.lbl.setText(msg)
