
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

        _menu_file    = self.addMenu("&File")

        _action = _menu_file.addAction("&New")
        _action.setIcon(SCR_GetIcon("f35b5975f6d636d7a6418bb4941edbdf89b80b55"))
        _action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_N))
        _action.triggered.connect(self.scrib.clbk_new)

        _action = _menu_file.addAction("&Open Test Folder")        
        _action.setIcon(SCR_GetIcon("b28971455cf45af0e2e37a9c33ca8ca01d5a660f"))
        _action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_O))
        _action.triggered.connect(self.scrib.clbk_load_testfolder)

        _menu_file.addSeparator()

        _action = _menu_file.addAction("&Save")
        _action.setIcon(SCR_GetIcon("eb1729093812c3f38a5e4eb2714f2bde148f6eba"))
        _action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_S))
        _action.triggered.connect(self.scrib.clbk_save)

        _menu_file.addSeparator()

        _menu_recents = _menu_file.addMenu("&Open Recent")
        _recents      = self.scrib.preferences.get("recents")

        if _recents != None:
            for _recent in _recents:
                _name = _recent
                if len(_recent) > 100:
                    _name = "...%s" % (_recent[100:])
                _action = _menu_recents.addAction("&%s" % (_name,))
                _action.setIcon(SCR_GetIcon("b28971455cf45af0e2e37a9c33ca8ca01d5a660f"))
                _action.triggered.connect(partial(self.scrib.sgn_load_testfolder.emit,_recent))

        _menu_file.addSeparator()

        _action = _menu_file.addAction("&Exit")
        _action.setIcon(SCR_GetIcon("325eab1e2242ef8223f4b2506db6da27384f3789"))
        _action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q))
        _action.triggered.connect(self.scrib.close)

    def populate_search(self):

        _menu_search = self.addMenu("&Search")

    def populate_plugins(self):

        _menu_plugins = self.addMenu("&Plugins")

    def populate_help(self):

        _menu_help = self.addMenu("&Help")

        _action = _menu_help.addAction("&Documentation")
        _action.setIcon(SCR_GetIcon("edaf568e98a4c6023a1d9eb657bc737cff2ef279"))
        _action.setShortcut(QKeySequence(Qt.Key_F1))

        _action = _menu_help.addAction("&Issue or Idea")
        _action.setIcon(SCR_GetIcon("68887170a19a6b6eb82e9a9346dd81efa8a67f4d"))

        _action = _menu_help.addAction("&About")
        _action.setIcon(SCR_GetIcon("fd2cf51bcbd304d61dbae1fdd954d4d1ec41e535"))