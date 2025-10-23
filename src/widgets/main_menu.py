"""
File contains all UI widgets regarding the Main Menu
"""

from PyQt6.QtCore          import *
from PyQt6.QtGui           import *
from PyQt6.QtWidgets       import * 
from widgets.widgets       import SCR_WDG_MenuBar
from functools             import partial

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_MainMenu(SCR_WDG_MenuBar):

    def __init__(self,config,scrib):

        SCR_WDG_MenuBar.__init__(self,config)

        self.scrib  = scrib
        self.config = config

    def populate(self,):

        self.populate_file()

        self.populate_tools()

        self.populate_plugins()

        self.populate_appearance()

        self.populate_help()

    def populate_file(self):

        _menu_file    = self.add_menu(self,"File")

        self.add_action(
                        _menu_file, 
                        "New",              
                        self.config.get_theme_icon_new(), 
                        QKeySequence("Ctrl+N"), 
                        self.scrib.act_file.new)

        self.add_action(
                        _menu_file, 
                        "Open Test Folder", 
                        self.config.get_theme_icon_folder(),
                        QKeySequence("Ctrl+O"), 
                        self.scrib.act_file.load_testfolder)

        self.add_action(
                        _menu_file, 
                        "Save",             
                        self.config.get_theme_icon_save(),
                        QKeySequence("Ctrl+S"), 
                        self.scrib.act_file.save)

        _menu_file.addSeparator()

        _menu_recents = self.add_menu(_menu_file,"&Open Recent")
        _recents      = self.scrib.preferences.get("recents")

        if _recents != None:

            for _recent in _recents:

                _name = _recent

                if len(_recent) > 100:

                    _name = "...{}".format(_recent[100:])

                self.add_action(
                                _menu_recents, 
                                _name,             
                                self.config.get_theme_icon_folder(), 
                                None, 
                                partial(self.scrib.act_file.load_testfolder_by_path,_recent))

        _menu_file.addSeparator()

        self.add_action(
                        _menu_file, 
                        "Exit",             
                        self.config.get_theme_icon_exit(), 
                        QKeySequence("Ctrl+Q"), 
                        self.scrib.close)

    def populate_tools(self):

        _menu_search = self.add_menu(self,"&Tools")

    def populate_appearance(self):

        _menu_appearance = self.add_menu(self,"&Appearance")

        _title = ""

        if self.scrib.preferences.get("theme") == "light":
            _title = "Theme Dark"
        else:
            _title = "Theme Light"

        self.add_action(
                        _menu_appearance, 
                        _title,              
                        self.config.get_theme_icon_theme(),
                        None, 
                        self.scrib.act_appearance.change_theme)

    def populate_plugins(self):

        _menu_plugins = self.add_menu(self,"&Plugins")

    def populate_help(self):

        _menu_help = self.add_menu(self,"&Help")

        self.add_action(
                        _menu_help, 
                        "Documentation",             
                        self.config.get_theme_icon_doc(), 
                        QKeySequence("Ctrl+F1"), 
                        self.scrib.act_help.help_documentation)

        self.add_action(
                        _menu_help, 
                        "Issue or Idea",             
                        self.config.get_theme_icon_bug(), 
                        None, 
                        self.scrib.act_help.help_issue)

        self.add_action(
                        _menu_help, 
                        "About",             
                        self.config.get_theme_icon_info(), 
                        None, 
                        self.scrib.act_help.help_about)





