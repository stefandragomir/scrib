
import os
from model.model                      import SCR_Base_List
from robot.api                        import get_tokens
from robot.api                        import get_model
from robot.parsing.model.blocks       import TestCaseSection
from robot.parsing.model.blocks       import VariableSection
from robot.parsing.model.blocks       import KeywordSection
from robot.parsing.model.blocks       import SettingSection
from robot.parsing.model.statements   import Variable
from robot.parsing.model.statements   import ResourceImport
from robot.parsing.model.blocks       import Keyword


"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control():

    def __init__(self):

        self.clear()

    def clear(self):

        self.testfolder = None
        self.resources  = SCR_Control_Resources()

    def read(self,path):

        self.testfolder = SCR_Control_Folder(self,path)

        self.testfolder.read(path)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control_Folder():

    def __init__(self,ctrl,path):

        self.path        = path
        self.name        = os.path.split(path)[1]
        self.dir         = os.path.split(path)[0]
        self.ctrl        = ctrl
        self.testfolders = SCR_Control_Folders()
        self.testsuites  = SCR_Control_TestSuites()
        self.resources   = SCR_Control_Resources()

    def read(self,path):

        for _item in os.listdir(self.path):

            _path = os.path.join(self.path,_item)

            if os.path.isdir(_path):

                self.read_testfolder(_path)

            else:

                if os.path.isfile(_path):

                    if os.path.splitext(_path)[1] == ".robot":

                      self.read_testsuite(_path)

                    else:

                        if os.path.splitext(_path)[1] == ".resource":

                           self.read_resource(_path)

    def read_testfolder(self,path):

        _testfolder = SCR_Control_Folder(self.ctrl,path)

        _testfolder.read(path)

        self.testfolders.add(_testfolder)

    def read_testsuite(self,path):

        _testsuite = SCR_Control_TestSuite(self.ctrl,path)

        _testsuite.read()

        self.testsuites.add(_testsuite)

    def read_resource(self,path):

        _resource = self.ctrl.resources.find_by_attribute("path",path)

        if _resource == None:

            _resource = SCR_Control_Resource(self.ctrl,path)

            _resource.read()

            self.ctrl.resources.add(_resource)

        self.resources.add(_resource)

    def has_files(self):

        return self.testfolders.has_files() or len(self.testsuites) != 0 or len(self.resources) != 0

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class _SCR_Control_With_Model():

    def __init__(self):

        self.model = None

    def is_section_testcases(self,section):

        return isinstance(section,TestCaseSection)

    def is_section_variables(self,section):

        return isinstance(section,VariableSection)

    def is_section_keywords(self,section):

        return isinstance(section,KeywordSection)        

    def is_section_settings(self,statement):

        return isinstance(statement,SettingSection)

    def is_statement_variable(self,statement):

        return isinstance(statement,Variable)

    def is_statement_keyword(self,statement):

        return isinstance(statement,Keyword)

    def is_statement_resource_import(self,statement):

        return isinstance(statement,ResourceImport)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control_Folders(SCR_Base_List):

    def __init__(self):

        SCR_Base_List.__init__(self)

    def has_files(self):

        return any([_folder.has_files() for _folder in self.objects])

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control_TestSuites(SCR_Base_List):

    def __init__(self):

        SCR_Base_List.__init__(self)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control_TestSuite(_SCR_Control_With_Model):

    def __init__(self,ctrl,path):

        _SCR_Control_With_Model.__init__(self)

        self.path      = path
        self.name      = os.path.splitext(os.path.split(path)[1])[0]
        self.dir       = os.path.split(path)[0]
        self.ctrl      = ctrl
        self.resources = SCR_Control_Resources()

    def read(self):

        self.model = get_model(source=self.path,data_only=False)

        for _section in self.model.sections:

            if self.is_section_settings(_section):

                for _item in _section.body:

                    if self.is_statement_resource_import(_item):

                        _path = os.path.abspath(os.path.join(self.dir,_item.name))

                        _resource = self.ctrl.resources.find_by_attribute("path",_path)

                        if _resource == None:

                            _resource = SCR_Control_Resource(self.ctrl,_path)

                        self.ctrl.resources.add(_resource)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control_Resources(SCR_Base_List):

    def __init__(self):

        SCR_Base_List.__init__(self)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control_Resource(_SCR_Control_With_Model):

    def __init__(self,ctrl,path):

        _SCR_Control_With_Model.__init__(self)

        self.path  = path
        self.name  = os.path.splitext(os.path.split(path)[1])[0]
        self.dir   = os.path.split(path)[0]
        self.ctrl  = ctrl

    def read(self):

        self.model = get_model(source=self.path,data_only=False)
        
"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""