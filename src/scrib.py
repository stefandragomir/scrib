
import os
import sys
import error.error
from PyQt6.QtCore             import *
from PyQt6.QtGui              import *
from PyQt6.QtWidgets          import * 
from widgets.widgets          import SCR_WDG_DockWidget
from widgets.widgets          import SCR_WDG_ToolBar
from widgets.widgets          import SCR_WDG_ActionBar
from widgets.status_bar       import SCR_WDG_MainStatusBar
from widgets.main_menu        import SCR_WDG_MainMenu
from widgets.test_tree        import SCR_WDG_TestTree_Widget
from widgets.test_tab         import SCR_WDG_Test_Tab
from widgets.console          import SCR_WDG_Console
from widgets.plugin_manager   import SCR_PluginManager
from actions.actions          import SCR_Actions_File
from actions.actions          import SCR_Actions_Tools
from actions.actions          import SCR_Actions_Appearance
from actions.actions          import SCR_Actions_Help
from config.config            import SCR_Config
from icons.icons              import SCR_GetIcon
from control.control          import SCR_Control
from preferences.preferences  import SCR_Preferences
from logger.logger            import SCR_Logger
from utils.utils              import scr_get_logger_dir
from messenger.messenger      import SCR_Messenger

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_UI(QMainWindow):

    def __init__(self,app,config):

        QMainWindow.__init__(self)

        self.app             = app
        self.config          = config
        self.logger          = SCR_Logger()
        self.messenger       = SCR_Messenger()
        self.preferences     = SCR_Preferences()

        self.preferences.load()
        self.configure_logger()
        self.configure_messenger()

        self.ctrl            = SCR_Control(self.logger)        
        self.act_file        = SCR_Actions_File(self,self.logger)
        self.act_tools       = SCR_Actions_Tools(self,self.logger)
        self.act_help        = SCR_Actions_Help(self,self.logger)
        self.act_appearance  = SCR_Actions_Appearance(self,self.logger)
        self.plugin_manager  = SCR_PluginManager(self.config,self.logger,self.preferences)
        self.console_visible = False

        self.plugin_manager.load_plugins()

        self.draw_gui()       

    def draw_gui(self):

        self.config.theme = self.preferences.get("theme")

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
        self.draw_console()
        self.draw_test_tab()   
        self.draw_main_menu()
        self.draw_status_bar()
        

        self.ly_h.addWidget(self.wdg_test_tab)

        self.ly.addWidget(self.wdg_toolbar)
        self.ly.addLayout(self.ly_h)
        self.ly.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.wdg_central.setLayout(self.ly)

        self.setCentralWidget(self.wdg_central)
        self.activateWindow()

    def draw_toolbar(self):

        self.wdg_toolbar = SCR_WDG_ToolBar(self.config)

        # self.wdg_toolbar.add_button(
        #                                 "load testfolder",
        #                                 self.config.get_theme_icon_folder(),
        #                                 self.config.get_theme_icon_folder(),
        #                                 "Load Tests Folder",
        #                                 self.act_file.load_testfolder)
        
        # self.wdg_toolbar.add_button(
        #                                 "save",
        #                                 self.config.get_theme_icon_save(),
        #                                 self.config.get_theme_icon_save(),
        #                                 "Save",
        #                                 self.act_file.save)
        self.wdg_toolbar.draw()

    def draw_test_tree(self):

        self.wdg_tree_test = SCR_WDG_TestTree_Widget(self.config,self)

        self.dock_tree_test = SCR_WDG_DockWidget(self.config)

        self.dock_tree_test.setWidget(self.wdg_tree_test)

        self.dock_tree_test.setFeatures(
                                        QDockWidget.DockWidgetFeature.DockWidgetMovable | 
                                        QDockWidget.DockWidgetFeature.DockWidgetFloatable)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,self.dock_tree_test)

    def draw_test_tab(self):

        self.wdg_test_tab = SCR_WDG_Test_Tab(
                                                self.config,
                                                self.plugin_manager.plugins)

        _policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        _policy.setHorizontalStretch(3)

        self.wdg_test_tab.setSizePolicy(_policy)

    def draw_main_menu(self):

        self.main_menu = SCR_WDG_MainMenu(self.config,self)

        self.main_menu.populate()

        self.setMenuBar(self.main_menu)

    def draw_status_bar(self):

        self.status_bar = SCR_WDG_MainStatusBar(self.app,self.config)

        self.setStatusBar(self.status_bar)

    def draw_console(self):

        self.wdg_console = SCR_WDG_Console(self.config)

        self.dock_console = SCR_WDG_DockWidget(self.config)

        self.dock_console.setWidget(self.wdg_console)

        self.dock_console.setFeatures(
                                        QDockWidget.DockWidgetFeature.DockWidgetMovable | 
                                        QDockWidget.DockWidgetFeature.DockWidgetFloatable)

        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea,self.dock_console)

        self.dock_console.hide()

        self.logger.set_ui(self.wdg_console)

    def configure_logger(self):

        _path = scr_get_logger_dir() 

        _path = os.path.join(_path,"log.txt")

        self.logger.set_debug_level(self.preferences.get("debug_logging"))

        self.logger.set_path(_path)        

    def configure_messenger(self):

        self.configure_messenger_test_tree()

        self.configure_messenger_main_menu()

        self.configure_messenger_new_items()

        self.configure_messenger_delete_items()

        self.configure_messenger_rename_items()

    def configure_messenger_test_tree(self):

        #used to signal that the Test Tree selected item (no matter the item) has changed
        #data - controller of object in tree
        self.messenger.create_message("TestTreeSelectionChange")

    def configure_messenger_main_menu(self):

        #used to signal that the Main Menu New option has been selected
        #data - path to the new test folder
        self.messenger.create_message("MainMenuNew")

        #used to signal that the Main Menu Open Test Folder or Recent Folder has been selected
        #data - path to the new test folder
        self.messenger.create_message("MainMenuOpenTestFolder")

        #used to signal that the Main Menu Save has been selected
        #data - None
        self.messenger.create_message("MainMenuSave")

        #used to signal that the Main Menu Show Console has been selected
        #data - None
        self.messenger.create_message("MainMenuShowConsole")

        #used to signal that the Main Menu Hide Console has been selected
        #data - None
        self.messenger.create_message("MainMenuHideConsole")

    def configure_messenger_new_items(self):

        #used to signal that a new Test Suite has been created
        #data - controller of new Test Suite
        self.messenger.create_message("NewTestSuite")

        #used to signal that a new Resource has been created
        #data - controller of new Resource
        self.messenger.create_message("NewResource")

        #used to signal that a new Test Case has been created
        #data - controller of new Test Case
        self.messenger.create_message("NewTestCase")

        #used to signal that a new Keyword has been created
        #data - controller of new Keyword
        self.messenger.create_message("NewTestKeyword")

        #used to signal that a new Scalar Variable has been created
        #data - controller of new Scalar Variable
        self.messenger.create_message("NewVariableScalar")

        #used to signal that a new List Variable has been created
        #data - controller of new List Variable
        self.messenger.create_message("NewVariableList")

        #used to signal that a new Dictionary Variable has been created
        #data - controller of new Dictionary Variable
        self.messenger.create_message("NewVariableDictionary")

    def configure_messenger_delete_items(self):

        #used to signal that a Test Suite has been deleted
        #data - controller of old Test Suite
        self.messenger.create_message("DeleteTestSuite")

        #used to signal that a Resource has been deleted
        #data - controller of old Resource
        self.messenger.create_message("DeleteResource")

        #used to signal that a Test Case has been deleted
        #data - controller of old Test Case
        self.messenger.create_message("DeleteTestCase")

        #used to signal that a Keyword has been deleted
        #data - controller of old Keyword
        self.messenger.create_message("DeleteTestKeyword")

        #used to signal that a Scalar Variable has been deleted
        #data - controller of old Scalar Variable
        self.messenger.create_message("DeleteVariableScalar")

        #used to signal that a List Variable has been deleted
        #data - controller of old List Variable
        self.messenger.create_message("DeleteVariableList")

        #used to signal that a Dictionary Variable has been deleted
        #data - controller of old Dictionary Variable
        self.messenger.create_message("DeleteVariableDictionary")

    def configure_messenger_rename_items(self):

        #used to signal that a Test Suite has been renamed
        #data - [controller of Test Suite, old name]
        self.messenger.create_message("RenameTestSuite")

        #used to signal that a Resource has been renamed
        #data - [controller of Resource, old name]
        self.messenger.create_message("RenameResource")

        #used to signal that a Test Case has been renamed
        #data - [controller of Test Case, old name]
        self.messenger.create_message("RenameTestCase")

        #used to signal that a Keyword has been renamed
        #data - [controller of Keyword, old name]
        self.messenger.create_message("RenameTestKeyword")

        #used to signal that a Scalar Variable has been renamed
        #data - [controller of Scalar Variable, old name]
        self.messenger.create_message("RenameVariableScalar")

        #used to signal that a List Variable has been renamed
        #data - [controller of List Variable, old name]
        self.messenger.create_message("RenameVariableList")

        #used to signal that a Dictionary Variable has been renamed
        #data - [controller of Dictionary Variable, old name]
        self.messenger.create_message("RenameVariableDictionary")

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
def SCR():

    sys.excepthook = error.error.SCR_Err_Net

    _app    = QApplication(sys.argv)  

    _config = SCR_Config()

    _ui     = SCR_UI(_app,_config)    

    _ui.show()

    sys.exit(_app.exec())

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
if __name__ == "__main__":

    SCR()


