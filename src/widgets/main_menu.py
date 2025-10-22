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
                        "f35b5975f6d636d7a6418bb4941edbdf89b80b55", 
                        QKeySequence("Ctrl+N"), 
                        self.scrib.act_file.new)

        self.add_action(
                        _menu_file, 
                        "Open Test Folder", 
                        "b28971455cf45af0e2e37a9c33ca8ca01d5a660f", 
                        QKeySequence("Ctrl+O"), 
                        self.scrib.act_file.load_testfolder)

        self.add_action(
                        _menu_file, 
                        "Save",             
                        "eb1729093812c3f38a5e4eb2714f2bde148f6eba", 
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
                                "b28971455cf45af0e2e37a9c33ca8ca01d5a660f", 
                                None, 
                                partial(self.scrib.act_file.load_testfolder_by_path,_recent))

        _menu_file.addSeparator()

        self.add_action(
                        _menu_file, 
                        "Exit",             
                        "325eab1e2242ef8223f4b2506db6da27384f3789", 
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
                        "f35b5975f6d636d7a6418bb4941edbdf89b80b55", 
                        None, 
                        self.scrib.act_appearance.change_theme)

    def populate_plugins(self):

        _menu_plugins = self.add_menu(self,"&Plugins")

    def populate_help(self):

        _menu_help = self.add_menu(self,"&Help")

        self.add_action(
                        _menu_help, 
                        "Documentation",             
                        "edaf568e98a4c6023a1d9eb657bc737cff2ef279", 
                        QKeySequence("Ctrl+F1"), 
                        self.scrib.act_help.help_documentation)

        self.add_action(
                        _menu_help, 
                        "Issue or Idea",             
                        "68887170a19a6b6eb82e9a9346dd81efa8a67f4d", 
                        None, 
                        self.scrib.act_help.help_issue)

        self.add_action(
                        _menu_help, 
                        "About",             
                        "fd2cf51bcbd304d61dbae1fdd954d4d1ec41e535", 
                        None, 
                        self.scrib.act_help.help_about)





