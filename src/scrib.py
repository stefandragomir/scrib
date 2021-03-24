
import os
import sys

from PyQt5.QtCore          import *
from PyQt5.QtGui           import *
from PyQt5.QtWidgets       import * 
from widgets.widgets       import SCR_WDG_DockWidget
from widgets.widgets       import SCR_WDG_ToolBar
from icons.icons           import SCR_GetIcon
from widgets.test_tree     import SCR_WDG_TestTree

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_UI(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        self.draw_gui() 

    def draw_gui(self):

        self.setWindowTitle("Robot Framework Scrib")
        self.setMinimumSize(1300, 800)       
        self.setMinimumHeight(500)
        self.setWindowIcon(SCR_GetIcon("356a192b7913b04c54574d18c28d46e6395428ab"))

        self.wdg_central = QWidget()

        self.ly = QVBoxLayout()

        self.draw_toolbar()

        self.ly.addWidget(self.wdg_toolbar)

        self.wdg_central.setLayout(self.ly)

        self.setCentralWidget(self.wdg_central)
        self.activateWindow()

    def draw_toolbar(self):

        self.wdg_toolbar = SCR_WDG_ToolBar()

        self.wdg_toolbar.add_button(
                                        "load",
                                        "da4b9237bacccdf19c0760cab7aec4a8359010b0",
                                        "1b6453892473a467d07372d45eb05abc2031647a",
                                        self.clbk_load)

        self.wdg_toolbar.add_button(
                                        "save",
                                        "77de68daecd823babbb58edb1c8e14d7106e83bb",
                                        "ac3478d69a3c81fa62e60f5c3696165a4e5e6ac4",
                                        self.clbk_save)
        self.wdg_toolbar.draw()

    def clbk_load(self,state):

        pass

    def clbk_save(self,state):

        pass

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
if __name__ == "__main__":

    _app = QApplication(sys.argv)  

    _ui  = SCR_UI()    

    _ui.show()

    sys.exit(_app.exec_())


