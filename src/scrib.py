
import os
import sys
import error.error
from PyQt5.QtCore          import *
from PyQt5.QtGui           import *
from PyQt5.QtWidgets       import * 
from config.config         import SCR_Config
from widgets.widgets       import SCR_WDG_DockWidget
from widgets.widgets       import SCR_WDG_ToolBar
from widgets.widgets       import SCR_WDG_StatusBar
from widgets.main_menu     import SCR_WDG_MainMenu
from icons.icons           import SCR_GetIcon
from widgets.test_tree     import SCR_WDG_TestTree
from widgets.test_tab      import SCR_WDG_Test_Tab
from widgets.status_bar    import SCR_WDG_Status_Bar
from control.control       import SCR_Control
from cache.preferences     import SCR_Preferences

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_UI(QMainWindow):

    sgn_load_testfolder = pyqtSignal(object)

    def __init__(self,app,config):

        QMainWindow.__init__(self)

        self.config      = config
        self.ctrl        = SCR_Control()
        self.app         = app
        self.preferences = SCR_Preferences()

        self.preferences.load()

        self.sgn_load_testfolder.connect(self.load_testfolder)

        self.draw_gui() 

    def draw_gui(self):

        self.setWindowTitle("Robot Framework Scrib")
        self.setMinimumSize(1300, 800)       
        self.setMinimumHeight(800)
        self.setWindowIcon(SCR_GetIcon("08e0c30ab7f9c6d43c70165c4ae42460d460c0aa"))
        self.setStyleSheet("background-color: %s; border: 0px;" % (self.config.get_theme_background()))

        self.wdg_central = QWidget()

        self.ly   = QVBoxLayout()
        self.ly_h = QHBoxLayout()

        self.draw_toolbar()
        self.draw_test_tree() 
        self.draw_test_tab()   
        self.draw_main_menu()
        self.draw_action_bar()
        self.draw_status_bar()

        self.ly_h.addWidget(self.wdg_tree_test)
        self.ly_h.addWidget(self.wdg_test_tab)

        self.ly.addWidget(self.wdg_toolbar)
        self.ly.addLayout(self.ly_h)
        self.ly.addWidget(self.action_bar)
        self.ly.setAlignment(Qt.AlignTop)

        self.wdg_central.setLayout(self.ly)

        self.setCentralWidget(self.wdg_central)
        self.activateWindow()

    def draw_toolbar(self):

        self.wdg_toolbar = SCR_WDG_ToolBar(self.config)



        self.wdg_toolbar.add_button(
                                        "load testfolder",
                                        "b28971455cf45af0e2e37a9c33ca8ca01d5a660f",
                                        "c9c73609abb7d353a69882826114ab5d501cc2bf",
                                        "Load Tests Folder",
                                        self.clbk_load_testfolder)
        
        self.wdg_toolbar.add_button(
                                        "save",
                                        "eb1729093812c3f38a5e4eb2714f2bde148f6eba",
                                        "0b5ff6fecdc20faffd3884561995dfa5bab539fd",
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

    def draw_main_menu(self):

        self.main_menu = SCR_WDG_MainMenu(self)

        self.main_menu.populate()

        self.setMenuBar(self.main_menu)

    def draw_action_bar(self):

        self.action_bar = SCR_WDG_StatusBar(self.app,self,self.config)

    def draw_status_bar(self):

        self.status_bar = SCR_WDG_Status_Bar(self.config)

        self.setStatusBar(self.status_bar)

    def clbk_new(self):

        pass

    def clbk_load_testfolder(self,state):

        _cwd = self.preferences.get("cwd")

        if _cwd == None:
            _cwd = ""

        _path = QFileDialog.getExistingDirectory(
                                                self,
                                                "Open Test Folder",
                                                _cwd)

        if os.path.exists(_path):

            self.sgn_load_testfolder.emit(_path)

    def clbk_save(self,state):

        pass

    def load_testfolder(self,path):

        if os.path.exists(path):

            self.action_bar.start(withload=False,withcancel=False)

            self.action_bar.msg("loading...")

            self.ctrl.read(path,self.action_bar)

            self.wdg_tree_test.clear()

            self.action_bar.msg("drawing test tree...")

            self.wdg_tree_test.populate(self.ctrl,["Tests"])

            self.action_bar.stop()

            self.status_bar.message("%s" % (path,))

            self.update_recent(path)

    def update_recent(self,path):

        _recents = self.preferences.get("recents")

        if _recents == None:
            _recents = []

        _recents.append(path)

        _recents = list(set(_recents))[-5:]

        self.preferences.set("recents",_recents)

        self.preferences.set("cwd",path)

        self.preferences.save()

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
def SCR():

    sys.excepthook = error.error.SCR_Err_Net

    _app    = QApplication(sys.argv)  

    _config = SCR_Config()

    _ui     = SCR_UI(_app,_config)    

    _ui.show()

    sys.exit(_app.exec_())

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
if __name__ == "__main__":

    SCR()


