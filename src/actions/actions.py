
import os

from PyQt6.QtCore          import *
from PyQt6.QtGui           import *
from PyQt6.QtWidgets       import *
from widgets.widgets       import SCR_WDG_PopUp

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Actions_File():

    def __init__(self,scrib,logger):

        self.scrib  = scrib
        self.logger = logger

    def new(self):

        pass

    def load_testfolder(self,state):

        _cwd = self.scrib.preferences.get("cwd")

        if _cwd == None:
            _cwd = ""

        _path = QFileDialog.getExistingDirectory(
                                                self.scrib,
                                                "Open Test Folder",
                                                _cwd)
        if os.path.exists(_path):

            self.load_testfolder_by_path(_path)

    def save(self,state):

        pass

    def load_testfolder_by_path(self,path):

        self.logger.info("load test folder by path [{}]".format(path))

        if os.path.exists(path):

            self.scrib.status_bar.start(withload=True,withcancel=False)

            self.scrib.status_bar.label("loading test folder")

            self.scrib.ctrl.read(path,self.scrib.status_bar)

            self.scrib.wdg_tree_test.wdg_tree.clear()

            self.scrib.status_bar.label("drawing test tree...")

            self.scrib.wdg_tree_test.wdg_tree.populate(self.scrib.ctrl,[""])

            self.scrib.status_bar.stop()

            self.scrib.status_bar.label("%s" % (path,))

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
class SCR_Actions_Tools():

    def __init__(self,scrib,logger):

        self.scrib  = scrib
        self.logger = logger

    def console_visibility(self):

        if self.scrib.console_visible:
            
            self.scrib.console_visible = False 
            self.scrib.dock_console.hide()
            self.scrib.main_menu.change_console_tile(False)
        else:

            self.scrib.console_visible = True
            self.scrib.dock_console.show()
            self.scrib.main_menu.change_console_tile(True)


"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Actions_Appearance():

    def __init__(self,scrib,logger):

        self.scrib  = scrib
        self.logger = logger

    def set_theme_light(self):

        self.scrib.preferences.set("theme","light")
        self.scrib.preferences.save()

        SCR_WDG_PopUp(
                        self.scrib.config,
                        "Apply Theme Light",
                        "Theme will be applied after Scrib is restarted")

    def set_theme_dark(self):

        self.scrib.preferences.set("theme","dark")
        self.scrib.preferences.save()

        SCR_WDG_PopUp(
                        self.scrib.config,
                        "Apply Theme Dark",
                        "Theme will be applied after Scrib is restarted")

    def set_theme_normal(self):

        self.scrib.preferences.set("theme","normal")
        self.scrib.preferences.save()

        SCR_WDG_PopUp(
                        self.scrib.config,
                        "Apply Theme Normal",
                        "Theme will be applied after Scrib is restarted")

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Actions_Help():

    def __init__(self,scrib,logger):

        self.scrib  = scrib
        self.logger = logger

    def help_documentation(self):

        QDesktopServices.openUrl(QUrl("https://github.com/stefandragomir/scrib/wiki"))

    def help_issue(self):

        QDesktopServices.openUrl(QUrl("https://github.com/stefandragomir/scrib/issues"))

    def help_about(self):

        pass

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Actions_Tree_TestFolder():

    def __init__(self,scrib):

        self.scrib     = scrib

    def new_test_suite(self,tree_item,data):

        self.scrib.wdg_tree_test.create_item(tree_item,"NewTestSuite")

    def new_resource(self,tree_item,data):

        pass

    def new_library(self,tree_item,data):

        pass

    def new_folder(self,tree_item,data):

        pass

    def delete(self,tree_item,data):

        pass

    def rename(self,tree_item,data):

        pass

    def sel_all(self,tree_item,data):

        pass

    def sel_all_failed(self,tree_item,data):

        pass

    def sel_all_passed(self,tree_item,data):

        pass

    def desel_all(self,tree_item,data):

        pass

    def desel_all_failed(self,tree_item,data):

        pass

    def desel_all_passed(self,tree_item,data):

        pass        

    def open(self,tree_item,data):

        pass

    def search(self,tree_item,data):

        pass

    def new_folder(self,tree_item,data):

        pass

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Actions_Tree_TestSuite():

    def __init__(self,scrib):

        self.scrib     = scrib

    def new_testcase(self,tree_item,data):

        pass

    def new_keyword(self,tree_item,data):

        pass

    def new_var_scalar(self,tree_item,data):

        pass

    def new_var_list(self,tree_item,data):

        pass

    def new_var_dict(self,tree_item,data):

        pass

    def delete(self,tree_item,data):

        pass

    def rename(self,tree_item,data):

        pass

    def sel_all(self,tree_item,data):

        pass

    def sel_all_failed(self,tree_item,data):

        pass

    def sel_all_passed(self,tree_item,data):

        pass

    def desel_all(self,tree_item,data):

        pass

    def desel_all_failed(self,tree_item,data):

        pass

    def desel_all_passed(self,tree_item,data):

        pass        

    def open(self,tree_item,data):

        pass

    def search(self,tree_item,data):

        pass

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Actions_Tree_Resource():

    def __init__(self,scrib):

        self.scrib     = scrib

    def new_keyword(self,tree_item,data):

        pass

    def new_var_scalar(self,tree_item,data):

        pass

    def new_var_list(self,tree_item,data):

        pass

    def new_var_dict(self,tree_item,data):

        pass

    def delete(self,tree_item,data):

        pass

    def rename(self,tree_item,data):

        pass

    def open(self,tree_item,data):

        pass

    def search(self,tree_item,data):

        pass

    def find_usage(self,tree_item,data):

        pass

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Actions_Tree_TestCase():

    def __init__(self,scrib):

        self.scrib     = scrib

    def delete(self,tree_item,data):

        pass

    def rename(self,tree_item,data):

        pass

    def moveup(self,tree_item,data):

        pass

    def movedown(self,tree_item,data):

        pass

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Actions_Tree_Keyword():

    def __init__(self,scrib):

        self.scrib     = scrib

    def delete(self,tree_item,data):

        pass

    def rename(self,tree_item,data):

        pass

    def moveup(self,tree_item,data):

        pass

    def movedown(self,tree_item,data):

        pass

    def find_usage(self,tree_item,data):

        pass

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Actions_Tree_Variable():

    def __init__(self,scrib):

        self.scrib     = scrib

    def delete(self,tree_item,data):

        pass

    def rename(self,tree_item,data):

        pass

    def moveup(self,tree_item,data):

        pass

    def movedown(self,tree_item,data):

        pass

    def find_usage(self,tree_item,data):

        pass

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Actions_Tree_Library():

    def __init__(self,scrib):

        self.scrib     = scrib

    def delete(self,tree_item,data):

        pass

    def rename(self,tree_item,data):

        pass

    def open(self,tree_item,data):

        pass

    def find_usage(self,tree_item,data):

        pass

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Actions_Tree_ExtResources():

    def __init__(self,scrib):

        self.scrib     = scrib

    def search(self,tree_item,data):

        pass

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Actions_Tree_ExtLibraries():

    def __init__(self,scrib):

        self.scrib     = scrib

    def search(self,tree_item,data):

        pass