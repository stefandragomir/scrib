
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
from widgets.test_tab      import SCR_WDG_Test_Tab
from control.control       import SCR_Control_TestSuite
from control.control       import SCR_Control_Folder

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_UI(QMainWindow):

    sgn_load_testsuite  = pyqtSignal(object)
    sgn_load_testfolder = pyqtSignal(object)

    def __init__(self,config):

        QMainWindow.__init__(self)

        self.config = config

        self.sgn_load_testsuite.connect(self.load_testsuite)
        self.sgn_load_testfolder.connect(self.load_testfolder)

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
        self.draw_test_tab()   

        self.ly_h.addWidget(self.wdg_tree_test)
        self.ly_h.addWidget(self.wdg_test_tab)

        self.ly.addWidget(self.wdg_toolbar)
        self.ly.addLayout(self.ly_h)
        self.ly.setAlignment(Qt.AlignTop)

        self.wdg_central.setLayout(self.ly)

        self.setCentralWidget(self.wdg_central)
        self.activateWindow()

    def draw_toolbar(self):

        self.wdg_toolbar = SCR_WDG_ToolBar(self.config)

        self.wdg_toolbar.add_button(
                                        "load testsuite",
                                        "49850f9d3d0a11fd301d3514913462eda50bfc92",
                                        "417538f47c04e8b72bd6534b36cf794640f56b0f",
                                        "Load Tests Suite",
                                        self.clbk_load_testsuite)

        self.wdg_toolbar.add_button(
                                        "load testfolder",
                                        "49850f9d3d0a11fd301d3514913462eda50bfc92",
                                        "417538f47c04e8b72bd6534b36cf794640f56b0f",
                                        "Load Tests Folder",
                                        self.clbk_load_testfolder)

        self.wdg_toolbar.add_button(
                                        "save",
                                        "54f702f45430bdb78c15c1a94196e85c1ec432ab",
                                        "2a2d5277ae393f65c3af483322f8055993228031",
                                        "Save",
                                        self.clbk_save)
        self.wdg_toolbar.draw()

    def draw_test_tree(self):

        self.wdg_tree_test = SCR_WDG_TestTree(self.config)

        _policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        _policy.setHorizontalStretch(1)

        self.wdg_tree_test.setSizePolicy(_policy)

    def draw_test_tab(self):

        self.wdg_test_tab = SCR_WDG_Test_Tab(self.config)

        _policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        _policy.setHorizontalStretch(3)

        self.wdg_test_tab.setSizePolicy(_policy)

    def clbk_load_testsuite(self,state):

        _path = QFileDialog.getOpenFileName(
                                                self,
                                                "Open Test Suite",
                                                "",
                                                "*.robot")

        _path = _path[0]

        if os.path.exists(_path):

            self.sgn_load_testsuite.emit(_path)

    def clbk_load_testfolder(self,state):

        _path = QFileDialog.getExistingDirectory(
                                                self,
                                                "Open Test Folder",
                                                "")

        if os.path.exists(_path):

            self.sgn_load_testfolder.emit(_path)

    def clbk_save(self,state):

        pass

    def clbk_save_all(self,state):

        pass

    def load_testsuite(self,path):

        if os.path.exists(path):

            _ctrl = SCR_Control_TestSuite(path)

            _ctrl.read()

            self.wdg_tree_test.populate(_ctrl,["Tests"])

    def load_testfolder(self,path):

        if os.path.exists(path):

            _ctrl = SCR_Control_Folder(path)

            _ctrl.read()

            self.wdg_tree_test.populate(_ctrl,["Tests"])

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


