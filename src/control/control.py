
import os
from model.model import SCR_Base_List
from robot.api   import get_tokens
from robot.api   import get_model

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
class SCR_Control_Folder(object):

    def __init__(self,path):

        self.path        = path
        self.name        = os.path.split(path)[1]
        self.testfolders = SCR_Control_Folders()
        self.testsuites  = SCR_Control_TestSuites()
        self.resources   = SCR_Control_Resources()

    def read(self):

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

        _testfolder = SCR_Control_Folder(path)

        _testfolder.read()

        self.testfolders.add(_testfolder)

    def read_testsuite(self,path):

        _testsuite = SCR_Control_TestSuite(path)

        _testsuite.read()

        self.testsuites.add(_testsuite)

    def read_resource(self,path):

        _testresource = SCR_Control_Resource(path)

        _testresource.read()

        self.resources.add(_testresource)

    def has_files(self):

        return self.testfolders.has_files() or len(self.testsuites) != 0 or len(self.resources) != 0

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control_TestSuites(SCR_Base_List):

    def __init__(self):

        SCR_Base_List.__init__(self)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control_TestSuite(object):

    def __init__(self,path):

        self.path  = path
        self.name  = os.path.splitext(os.path.split(path)[1])[0]
        self.model = None

    def read(self):

        self.model = get_model(source=self.path,data_only=False)

        # for _section in self.model.sections:

        #   print("SECTION: ",_section)

        #   for _body in _section.body:

        #       print("BODY--: ",_body)

        #   print("--------------------")

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control_Resources(SCR_Base_List):

    def __init__(self):

        SCR_Base_List.__init__(self)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control_Resource(object):

    def __init__(self,path):

        self.path  = path
        self.model = None

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""