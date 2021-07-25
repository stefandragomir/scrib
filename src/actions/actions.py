
import os

from PyQt5.QtCore          import *
from PyQt5.QtGui           import *
from PyQt5.QtWidgets       import *

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Actions_File():

    def __init__(self,scrib):

        self.scrib = scrib

    def clbk_new(self):

        pass

    def clbk_load_testfolder(self,state):

        _cwd = self.scrib.preferences.get("cwd")

        if _cwd == None:
            _cwd = ""

        _path = QFileDialog.getExistingDirectory(
                                                self.scrib,
                                                "Open Test Folder",
                                                _cwd)

        if os.path.exists(_path):

            self.load_testfolder(_path)

    def clbk_save(self,state):

        pass

    def load_testfolder(self,path):

        if os.path.exists(path):

            self.scrib.action_bar.start(withload=False,withcancel=False)

            self.scrib.action_bar.msg("loading...")

            self.scrib.ctrl.read(path,self.scrib.action_bar)

            self.scrib.wdg_tree_test.clear()

            self.scrib.action_bar.msg("drawing test tree...")

            self.scrib.wdg_tree_test.populate(self.scrib.ctrl,["Tests"])

            self.scrib.action_bar.stop()

            self.scrib.status_bar.message("%s" % (path,))

            _recents = self.scrib.preferences.get("recents")

            if _recents == None:
                _recents = []

            _recents.append(path)

            _recents = list(set(_recents))[-5:]

            self.scrib.preferences.set("recents",_recents)

            self.scrib.preferences.set("cwd",path)

            self.scrib.preferences.save()

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Actions_Help():

    def __init__(self,scrib):

        self.scrib = scrib

    def clbk_help_documentation(self):

        QDesktopServices.openUrl(QUrl("https://github.com/stefandragomir/scrib/wiki"))

    def clbk_help_issue(self):

        QDesktopServices.openUrl(QUrl("https://github.com/stefandragomir/scrib/issues"))

    def clbk_help_about(self):

        pass