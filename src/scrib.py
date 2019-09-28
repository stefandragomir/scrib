
import os
import sys

try:
    _path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
    sys.path.append(_path)
except:
    pass

_path = os.path.split(os.path.split(os.path.abspath("__file__"))[0])[0]
sys.path.append(_path)

from PyQt5.QtCore                                                      import *
from PyQt5.QtGui                                                       import *
from PyQt5.QtWidgets                                                   import * 
from ui.widgets.scr_widgets                                            import SCR_WDG_DockWidget
from ui.widgets.scr_widgets                                            import SCR_WDG_ToolBar

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_UI(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        self.draw_gui() 

    def draw_gui(self):
        #Define Ghost Manager interface aspect

        self.setWindowTitle("Robot Framework Scrib")
        self.setMinimumSize(1300, 800)       
        self.setMinimumHeight(500)

        self.wdg_central = QWidget()

        self.setCentralWidget(self.wdg_central)
        self.activateWindow()

        self.setAnimated(True)
        self.setDockOptions(QMainWindow.AnimatedDocks)

    def create_docks(self):

        self.dock_tree  = SCR_WDG_DockWidget()
        self.dock_tree.setTitleBarWidget(self.toolbar)
        self.dock_tree.setWidget(self.tree_tabs)
        self.dock_tree.setMinimumWidth(330)
        self.dock_tree.setFeatures(SCR_WDG_DockWidget.NoDockWidgetFeatures | SCR_WDG_DockWidget.DockWidgetMovable)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_tree )
        self.dock_tree.dockLocationChanged.connect(self.clbk_dock_location)

    def create_toolbar(self):

        self.toolbar = SCR_WDG_ToolBar(self)
        self.toolbar.setObjectName("toolbar")
        self.toolbar.setFloatable(False)
        self.toolbar.setIconSize(QSize(24, 24))
        self.toolbar.setMinimumHeight(30)
        self.toolbar.setOrientation(Qt.Horizontal)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
        # new_action = self.toolbar.addAction(SHICON("shade_new"), "New Shade Project")
        # new_action.triggered.connect(self._menu._handle_file_new_cfg)

        # open_action = self.toolbar.addAction(SHICON("shade_open"), "Open Shade Project")
        # open_action.triggered.connect(self._menu._handle_file_open_cfg)

        # save_action = self.toolbar.addAction(SHICON("shade_save"), "Save Shade Project")
        # save_action.triggered.connect(self._menu._handle_file_saveall_cfg)

        # self.toolbar.addAction(new_action)
        # self.toolbar.addAction(open_action)
        # self.toolbar.addAction(
        save_action)
        
        # self.toolbar.addSeparator()
        # self.toolbar.addAction(find_action)         
        
        # spacer = QWidget()                  #add expanding spacer in toolbar
        # spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.toolbar.addWidget(spacer)

        # #self.toolbar.addAction(self.diag_action)   
        # self.toolbar.addSeparator()
        # self.toolbar.addAction(self.build_action)

    def clbk_dock_location(self, area):
        '''set tabs position according to tree location'''
        if area == Qt.LeftDockWidgetArea:
            self.console.write_to_console('Moved Tree Dock to LEFT',LOG_SH_DEBUG_MEDIUM)
            self._tabs.setTabPosition(QTabWidget.West)

        elif area == Qt.RightDockWidgetArea:
            self.console.write_to_console('Moved Tree Dock to RIGHT',LOG_SH_DEBUG_MEDIUM)
            self._tabs.setTabPosition(QTabWidget.East)

        elif area == Qt.TopDockWidgetArea:
            self.console.write_to_console('Moved Tree Dock to TOP',LOG_SH_DEBUG_MEDIUM)
            self._tabs.setTabPosition(QTabWidget.North)

        elif area == Qt.BottomDockWidgetArea:
            self.console.write_to_console('Moved Tree Dock to BOTTOM',LOG_SH_DEBUG_MEDIUM)
            self._tabs.setTabPosition(QTabWidget.South)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
if __name__ == "__main__":

    _app = QApplication(sys.argv)  
    _ui  = SCR_UI()           
    _ui.show()
    sys.exit(_app.exec_())


