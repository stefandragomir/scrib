
import os
import sys
import error.error
from PyQt5.QtCore          import *
from PyQt5.QtGui           import *
from PyQt5.QtWidgets       import * 
from config.config         import SCR_Config
from widgets.widgets       import SCR_WDG_DockWidget
from widgets.widgets       import SCR_WDG_ToolBar
from icons.icons           import SCR_GetIcon
from widgets.test_tree     import SCR_WDG_TestTree
from widgets.widgets       import SCR_WDG_Tab

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_UI(QMainWindow):

    def __init__(self,config):

        QMainWindow.__init__(self)

        self.config = config

        self.draw_gui() 

    def draw_gui(self):

        self.setWindowTitle("Robot Framework Scrib")
        self.setMinimumSize(1300, 800)       
        self.setMinimumHeight(500)
        self.setWindowIcon(SCR_GetIcon("08e0c30ab7f9c6d43c70165c4ae42460d460c0aa"))
        self.setStyleSheet("background-color: %s; border: 0px;" % (self.config.get_theme_background()))

        self.wdg_central = QWidget()

        self.ly   = QVBoxLayout()
        self.ly_h = QHBoxLayout()

        self.draw_toolbar()
        self.draw_test_tree() 
        self.draw_tab()   

        self.ly_h.addWidget(self.wdg_tree_test)
        self.ly_h.addWidget(self.wdg_tab)

        self.ly.addWidget(self.wdg_toolbar)
        self.ly.addLayout(self.ly_h)
        self.ly.setAlignment(Qt.AlignTop)

        self.wdg_central.setLayout(self.ly)

        self.setCentralWidget(self.wdg_central)
        self.activateWindow()

    def draw_toolbar(self):

        self.wdg_toolbar = SCR_WDG_ToolBar(self.config)

        self.wdg_toolbar.add_button(
                                        "load",
                                        "8995d597af7135f3e133a116a7c6e8f603434af4",
                                        "8995d597af7135f3e133a116a7c6e8f603434af4",
                                        "Load Tests Folder",
                                        self.clbk_load)

        self.wdg_toolbar.add_button(
                                        "save",
                                        "8995d597af7135f3e133a116a7c6e8f603434af4",
                                        "8995d597af7135f3e133a116a7c6e8f603434af4",
                                        "Save",
                                        self.clbk_save)
        self.wdg_toolbar.draw()

    def draw_test_tree(self):

        self.wdg_tree_test = SCR_WDG_TestTree(self.config)

        _policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        _policy.setHorizontalStretch(1)

        self.wdg_tree_test.setSizePolicy(_policy)

    def draw_tab(self):

        self.wdg_tab = SCR_WDG_Tab(self.config)

        _policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        _policy.setHorizontalStretch(3)

        self.wdg_tab.setSizePolicy(_policy)

    def clbk_load(self,state):

        pass

    def clbk_save(self,state):

        pass

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
def SCR():

    sys.excepthook = error.error.SCR_Err_Net

    _app    = QApplication(sys.argv)  

    _config = SCR_Config()

    _ui     = SCR_UI(_config)    

    _ui.show()

    sys.exit(_app.exec_())

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
if __name__ == "__main__":

    SCR()


