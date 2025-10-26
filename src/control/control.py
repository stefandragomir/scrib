
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
from robot.parsing.model.statements   import LibraryImport
from robot.parsing.model.blocks       import Keyword
from utils.utils                      import get_all_folders
from utils.utils                      import get_all_files
from utils.utils                      import SCR_UtilProgress


from time import sleep

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control():

    def __init__(self,logger):

        self.logger = logger

        self.clear()

    def clear(self):

        self.testfolder  = None
        self.resources   = SCR_Control_Resources()
        self.libraries   = SCR_Control_Libraries()

    def read(self,path,observer):

        self.logger.debug("load test folder by path [{}]".format(path))

        self.testfolder = SCR_Control_Folder(
                                                parent=self,
                                                main_ctrl=self,
                                                path=path)

        _nr_of_items = len(get_all_files(path,None))
        _nr_of_items += len(get_all_folders(path)) - 1

        _progress = SCR_UtilProgress(_nr_of_items)

        self.testfolder.read(
                                path=path,
                                observer=observer,
                                progress=_progress)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class _SCR_Control_Base():

    def __init__(self,path,name,folder,parent,main_ctrl,model,ctrl_type):

        self.path      = path
        self.name      = name
        self.dir       = folder
        self.ctrl      = parent  
        self.main_ctrl = main_ctrl      
        self.model     = model
        self.ctrl_type = ctrl_type

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

    def is_statement_library_import(self,statement):

        return isinstance(statement,LibraryImport)

    def get_status_label(self):

        _text = "[{}]   [{}]".format(self.ctrl_type,self.path)

        return _text

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
class SCR_Control_Folder(_SCR_Control_Base):

    def __init__(self,parent,main_ctrl,path):

        _SCR_Control_Base.__init__(
                                    self,
                                    path=path,
                                    name=os.path.split(path)[1],
                                    folder=os.path.split(path)[0],
                                    parent=parent,
                                    main_ctrl=main_ctrl,
                                    model=None,
                                    ctrl_type="Test Folder")

        self.testfolders = SCR_Control_Folders()
        self.testsuites  = SCR_Control_TestSuites()
        self.resources   = SCR_Control_Resources()
        self.libraries   = SCR_Control_Libraries()

    def read(self,path,observer,progress):

        if None != observer:

            observer.message("reading test folder %s" % (self.name,))

        for _item in os.listdir(self.path):

            _path = os.path.join(self.path,_item)

            progress.increment()

            if None != observer:

                observer.progress(progress.get_progress())

            if os.path.isdir(_path):

                self.read_testfolder(_path,observer,progress)

            else:

                if os.path.isfile(_path):

                    if os.path.splitext(_path)[1] == ".robot":

                      self.read_testsuite(_path,observer)

                    else:

                        if os.path.splitext(_path)[1] == ".resource":

                           self.read_resource(_path,observer)

                        else:
                            if os.path.splitext(_path)[1] == ".py":

                                self.read_library(_path,observer)

    def read_testfolder(self,path,observer,progress):

        _testfolder = SCR_Control_Folder(
                                            parent=self,
                                            main_ctrl=self.main_ctrl,
                                            path=path)

        _testfolder.read(path,observer,progress)

        self.testfolders.add(_testfolder)

    def read_testsuite(self,path,observer):

        _testsuite = SCR_Control_TestSuite(
                                            parent=self,
                                            main_ctrl=self.main_ctrl,
                                            path=path)

        _testsuite.read(observer)

        self.testsuites.add(_testsuite)

    def read_resource(self,path,observer):

        _resource = SCR_Control_Resource(   
                                            parent=self,
                                            main_ctrl=self.main_ctrl,
                                            path=path)

        _resource.read(observer)

        self.main_ctrl.resources.add(_resource)

        self.resources.add(_resource)

    def read_library(self,path,observer):

        _library = SCR_Control_Library(
                                        parent=self,
                                        main_ctrl=main_ctrl,
                                        path=path)

        _library.read(observer)

        self.main_ctrl.libraries.add(_library)

        self.libraries.add(_library)

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
class SCR_Control_TestSuite(_SCR_Control_Base):

    def __init__(self,parent,main_ctrl,path):

        _SCR_Control_Base.__init__(
                                    self,
                                    path=path,
                                    name=os.path.splitext(os.path.split(path)[1])[0],
                                    folder=os.path.split(path)[0],
                                    parent=parent,
                                    main_ctrl=main_ctrl,
                                    model=None,
                                    ctrl_type="Test Suite")

    def read(self,observer):

        if None != observer:

            observer.message("reading test suite %s" % (self.name,))

        self.model = get_model(source=self.path,data_only=False)

        self.read_resources(observer)

    def read_resources(self,observer):

        for _section in self.model.sections:

            if self.is_section_settings(_section):

                for _item in _section.body:

                    if self.is_statement_resource_import(_item):

                        _path = os.path.abspath(os.path.join(self.dir,_item.name))

                        _resource = self.main_ctrl.resources.find_by_attribute("path",_path)

                        if _resource == None:

                            _resource = SCR_Control_Resource(
                                                                parent=self,
                                                                main_ctrl=self.main_ctrl,
                                                                path=_path)

                            _resource.read(observer)

                            self.main_ctrl.resources.add(_resource)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control_Resources(SCR_Base_List):

    def __init__(self):

        SCR_Base_List.__init__(self)

    def external(self):

        _resources = SCR_Control_Resources()

        _resources.objects = [_resource for _resource in self.objects if _resource.external]

        return _resources

    def internal(self):

        _resources = SCR_Control_Resources()

        _resources.objects = [_resource for _resource in self.objects if not _resource.external]

        return _resources

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control_Resource(_SCR_Control_Base):

    def __init__(self,parent,main_ctrl,path):

        _SCR_Control_Base.__init__(
                                    self,
                                    path=path,
                                    name=os.path.splitext(os.path.split(path)[1])[0],
                                    folder=os.path.split(path)[0],
                                    parent=parent,
                                    main_ctrl=main_ctrl,
                                    model=None,
                                    ctrl_type="Test Resource")

        self.external = not os.path.abspath(path).startswith(os.path.abspath(main_ctrl.testfolder.path))

    def read(self,observer):

        if None != observer:

            observer.message("reading resource %s" % (self.name,))

        self.model = get_model(source=self.path,data_only=False)

        self.read_resources(observer)

        self.read_libraries(observer)

    def read_resources(self,observer):

        for _section in self.model.sections:

            if self.is_section_settings(_section):

                for _item in _section.body:

                    if self.is_statement_resource_import(_item):

                        _path = os.path.abspath(os.path.join(self.dir,_item.name))

                        if os.path.exists(_path):

                            _resource = self.main_ctrl.resources.find_by_attribute("path",_path)

                            if _resource == None:

                                _resource = SCR_Control_Resource(
                                                                    parent=self,
                                                                    main_ctrl=self.main_ctrl,
                                                                    path=_path)

                                _resource.read(observer)

                                self.main_ctrl.resources.add(_resource)

    def read_libraries(self,observer):

        for _section in self.model.sections:

            if self.is_section_settings(_section):

                for _item in _section.body:

                    if self.is_statement_library_import(_item):

                        _path = os.path.abspath(os.path.join(self.dir,_item.name))

                        if os.path.exists(_path):

                            _library = self.main_ctrl.libraries.find_by_attribute("path",_path)

                            if _library == None:

                                _library = SCR_Control_Library(
                                                                parent=self,
                                                                main_ctrl=self.main_ctrl,
                                                                path=_path)

                                _library.read(observer)

                                self.main_ctrl.libraries.add(_library)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control_Libraries(SCR_Base_List):

    def __init__(self):

        SCR_Base_List.__init__(self)

    def external(self):

        _libraries = SCR_Control_Libraries()

        _libraries.objects = [_library for _library in self.objects if _library.external]

        return _libraries

    def internal(self):

        _libraries = SCR_Control_Libraries()

        _libraries.objects = [_library for _library in self.objects if not _library.external]

        return _libraries

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control_Library(_SCR_Control_Base):

    def __init__(self,parent,main_ctrl,path):

        _SCR_Control_Base.__init__(
                                    self,
                                    path=path,
                                    name=os.path.splitext(os.path.split(path)[1])[0],
                                    folder=os.path.split(path)[0],
                                    parent=parent,
                                    main_ctrl=main_ctrl,
                                    model=None,
                                    ctrl_type="Test Library")

        self.external = not os.path.abspath(path).startswith(os.path.abspath(main_ctrl.testfolder.path))

    def read(self,observer):

        if None != observer:

            observer.message("reading library %s" % (self.name,))
                       
"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""