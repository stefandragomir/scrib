
from PyQt5.QtCore          import *
from PyQt5.QtGui           import *
from PyQt5.QtWidgets       import * 
from icons.icons           import SCR_GetIcon
from functools             import partial

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_MainMenu(QMenuBar):

    def __init__(self,scrib):

        QMenuBar.__init__(self,scrib)

        self.scrib = scrib

    def populate(self,):

        self.populate_file()

        # self.populate_search()

        # self.populate_plugins()

        self.populate_help()

    def populate_file(self):

        _menu_file    = self.addMenu("File")

        self.add_action(
                        _menu_file, 
                        "New",              
                        "f35b5975f6d636d7a6418bb4941edbdf89b80b55", 
                        QKeySequence(Qt.CTRL + Qt.Key_N), 
                        self.scrib.act_file.clbk_new)

        self.add_action(
                        _menu_file, 
                        "Open Test Folder", 
                        "b28971455cf45af0e2e37a9c33ca8ca01d5a660f", 
                        QKeySequence(Qt.CTRL + Qt.Key_O), 
                        self.scrib.act_file.clbk_load_testfolder)

        self.add_action(
                        _menu_file, 
                        "Save",             
                        "eb1729093812c3f38a5e4eb2714f2bde148f6eba", 
                        QKeySequence(Qt.CTRL + Qt.Key_S), 
                        self.scrib.act_file.clbk_save)

        _menu_file.addSeparator()

        _menu_recents = _menu_file.addMenu("&Open Recent")
        _recents      = self.scrib.preferences.get("recents")

        if _recents != None:
            for _recent in _recents:
                _name = _recent
                if len(_recent) > 100:
                    _name = "...%s" % (_recent[100:])

                self.add_action(
                                _menu_recents, 
                                _name,             
                                "b28971455cf45af0e2e37a9c33ca8ca01d5a660f", 
                                None, 
                                partial(self.scrib.act_file.load_testfolder,_recent))

        _menu_file.addSeparator()

        self.add_action(
                        _menu_file, 
                        "Exit",             
                        "325eab1e2242ef8223f4b2506db6da27384f3789", 
                        QKeySequence(Qt.CTRL + Qt.Key_Q), 
                        self.scrib.close)

    def populate_search(self):

        _menu_search = self.addMenu("&Search")

    def populate_plugins(self):

        _menu_plugins = self.addMenu("&Plugins")

    def populate_help(self):

        _menu_help = self.addMenu("&Help")

        self.add_action(
                        _menu_help, 
                        "Documentation",             
                        "edaf568e98a4c6023a1d9eb657bc737cff2ef279", 
                        QKeySequence(Qt.CTRL + Qt.Key_F1), 
                        self.scrib.act_help.clbk_help_documentation)

        self.add_action(
                        _menu_help, 
                        "Issue or Idea",             
                        "68887170a19a6b6eb82e9a9346dd81efa8a67f4d", 
                        None, 
                        self.scrib.act_help.clbk_help_issue)

        self.add_action(
                        _menu_help, 
                        "About",             
                        "fd2cf51bcbd304d61dbae1fdd954d4d1ec41e535", 
                        None, 
                        self.scrib.act_help.clbk_help_about)

    def add_action(self,parent,text,icon,shortcut,callback):

        _action = QAction(parent)
        _action.setText(text)
        _action.setIcon(SCR_GetIcon(icon))

        if shortcut != None:
            _action.setShortcut(shortcut)

        _action.triggered.connect(callback)
        parent.addAction(_action)



