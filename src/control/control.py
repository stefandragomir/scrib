
import os

from abc          import abstractmethod
from utils.utils  import get_all_folders
from utils.utils  import get_all_files
from utils.utils  import SCR_UtilProgress
from model.model  import SCR_Base_List
from model.model  import SCR_Model_Folder
from model.model  import SCR_Model_TestSuite
from model.model  import SCR_Model_Resource
from model.model  import SCR_Model_TestCase
from model.model  import SCR_Model_Variable
from model.model  import SCR_Model_Keyword
from model.model  import SCR_Model_Library
from model.model  import SCR_Model_Error

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control():

    def __init__(self,logger):

        self.logger = logger

        self.clear()

    def clear(self):

        #control tree, used to recurse inside the control structure
        self.testfolder  = None

        #list of all items in the control. usefull for searching
        self.testsuites  = SCR_Control_TestSuites()
        self.testcases   = SCR_Control_TestCases()
        self.keywords    = SCR_Control_Keywords()
        self.variables   = SCR_Control_Variables()
        self.resources   = SCR_Control_Resources()
        self.libraries   = SCR_Control_Libraries()      
        
    def read(self,path,observer):

        self.logger.debug("load test folder by path [{}]".format(path))

        #create the root item of the control
        #holds the controller for the folder loaded
        self.testfolder = SCR_Control_Folder(
                                                parent=self,
                                                main_ctrl=self,
                                                path=path,
                                                logger=self.logger)

        #get the number of folders and files that need to be loaded
        #will be used in progress status
        _nr_of_items = len(get_all_files(path,None))
        _nr_of_items += len(get_all_folders(path)) - 1

        #imutable progress items used by recursive calls to track progress
        _progress = SCR_UtilProgress(_nr_of_items)

        #start loading folders and files
        self.testfolder.read(
                                path=path,
                                observer=observer,
                                progress=_progress)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class _SCR_Control_Base():

    def __init__(self,path,name,folder,parent,main_ctrl,model,ctrl_type,logger):

        self.path      = path
        self.name      = name
        self.folder    = folder
        self.parent    = parent  
        self.main_ctrl = main_ctrl      
        self.model     = model
        self.ctrl_type = ctrl_type
        self.logger    = logger

    def get_status_label(self):

        #this label will be used by the ui status bar (at the bottom) 
        #to show what element is selected
        _text = "[{}]   [{}]".format(self.ctrl_type,self.path)

        return _text

    @abstractmethod
    def validate(self):

        raise NotImplementedError

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class _SCR_Control_WitTable(_SCR_Control_Base):
    """
    Used by controllers that contain statements (calls, assignments)
    Used for Test Cases and Keywords
    """

    def __init__(self,path,name,folder,parent,main_ctrl,model,ctrl_type,logger):

        _SCR_Control_Base.__init__(
                                    self,
                                    path=path,
                                    name=name,
                                    folder=folder,
                                    parent=parent,
                                    main_ctrl=main_ctrl,
                                    model=model,
                                    ctrl_type=ctrl_type,
                                    logger=logger)

    def get_nr_of_rows(self):

        #number of row is the number of statements minus the last one (EOF)
        #added one more row for visual reasons and editing
        return self.model.get_nr_of_statements() + 1

    def get_nr_of_columns(self):

        #number of columns is the maximum number of cells used by any statement
        #added one more column vor visual reasons and editing
        return self.model.get_max_statement_size() + 1

    def get_cell_text(self,row,column):

        #get the actual text in the rf statement at row and column
        return self.model.get_statement_text_by_index(row)[column]

    def get_column_counts(self):
        """
        Get the number of columns needed for each statement
        """

        _count = []

        _statements = self.model.get_statements()

        for _statement in _statements:

            _count.append(self.model.get_statement_size(_statement))

        return _count

    def is_valid(self):
        """
        Return True or Fals if the entire model (Test Case or Keyword) is valid or not
        """

        return self.model.valid

    def is_keyword_name(self,row,column):
        """
        Return True if the cell contains a keyword name
        """

        #get the rf statement on this row
        _statement = self.model.get_statement_by_index(row)

        return self.model.is_cell_keyword_call_name(_statement,column)

    def is_keyword_assignment(self,row,column):
        """
        Returns True if the cell contains a keyword assignment (usually a variable of some type)
        """

        #get the rf statement on this row
        _statement = self.model.get_statement_by_index(row)

        return self.model.is_cell_keyword_call_assignment(_statement,column)

    def validate(self,row,column):
        """
        Check if a single statement cell is valid or invalid
        Valid - no syntax error
        Invalid - has a syntax error and an error text
        """

        _valid = False

        #get the rf statement on this row
        _statement = self.model.get_statement_by_index(row)

        #ask the model if the statement on this row is a keyword call
        if self.model.is_statement_keyword_call(_statement):

            #check if the cell in the statement is valid
            _valid = self.validate_keyword_call(_statement,row,column)

        return _valid

    def validate_keyword_call(self,statement,row,column):
        """
        Check if the keyword call statement cell is valid
        """

        _valid = False

        if self.model.is_cell_keyword_call_name(statement,column):

            _valid = self.validate_keyword_call_name(statement,row,column)
        else:
            if self.model.is_cell_keyword_call_assignment(statement,column):

                _valid = self.validate_keyword_call_assignment(statement,row,column)
            else:
                _valid = self.validate_keyword_call_argument(statement,row,column)

        return _valid

    def validate_keyword_call_name(self,statement,row,column):
        """
        Check if the keyword call name in the statement is valid
        """

        _valid = False

        _keywords_db = []

        #get the name of the keyword
        _keyword_name = self.model.get_statement_keyword_name(statement)

        #get the names of all keywords in the parent (Resource or Test Suite)
        _keywords_db += [_keyword.name for _keyword in self.parent.keywords]

        #get the names of all keywords in the parent imported resources
        for _resource in self.parent.resources:

            _keywords_db += [_keyword.name for _keyword in _resource.keywords]

        if _keyword_name in _keywords_db:

            _valid = True

        else:
            self.model.add_error(
                                    row,
                                    column,
                                    SCR_Model_Error.ERROR_UNKNOWN_KEYWORD,
                                    _keyword_name)

            #invalidate entire model
            self.model.valid = False

            _valid = False

        return _valid

    def validate_keyword_call_assignment(self,statement,row,column):
        """
        Check if a keyword call assignment cell in the statement is valid
        """

        _valid = True

        return _valid

    def validate_keyword_call_argument(self,statement,row,column):
        """
        Check if a keyword call argument cell in the statement is valid
        """

        _valid = True

        return _valid

    def get_error_text(self,row,column):
        """
        Return the error text of a cell in the statement
        Used for tooltips
        """

        _text = ""

        for _error in self.model.errors:

            if _error.row == row and _error.column == column:

                _text += "{}\n".format(_error.text)

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

    def __init__(self,parent,main_ctrl,path,logger):

        _SCR_Control_Base.__init__(
                                    self,
                                    path=path,
                                    name=os.path.split(path)[1],
                                    folder=os.path.split(path)[0],
                                    parent=parent,
                                    main_ctrl=main_ctrl,
                                    model=SCR_Model_Folder(),
                                    ctrl_type="Test Folder",
                                    logger=logger)

        self.testfolders = SCR_Control_Folders()
        self.testsuites  = SCR_Control_TestSuites()
        self.resources   = SCR_Control_Resources()
        self.libraries   = SCR_Control_Libraries()

    def read(self,path,observer,progress):

        self.logger.debug("reading test folder [{}]".format(path))

        if None != observer:

            observer.message("reading test folder {}".format(self.name,))

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
                                            path=path,
                                            logger=self.logger)

        _testfolder.read(path,observer,progress)

        self.testfolders.add(_testfolder)

    def read_testsuite(self,path,observer):

        _testsuite = SCR_Control_TestSuite(
                                            parent=self,
                                            main_ctrl=self.main_ctrl,
                                            path=path,
                                            logger=self.logger)

        _testsuite.read(observer)

        self.testsuites.add(_testsuite)

    def read_resource(self,path,observer):

        _resource = SCR_Control_Resource(   
                                            parent=self,
                                            main_ctrl=self.main_ctrl,
                                            path=path,
                                            logger=self.logger)

        _resource.read(observer)

        self.main_ctrl.resources.add(_resource)

        self.resources.add(_resource)

    def read_library(self,path,observer):

        _library = SCR_Control_Library(
                                        parent=self,
                                        main_ctrl=main_ctrl,
                                        path=path,
                                        logger=self.logger)

        _library.read(observer)

        self.main_ctrl.libraries.add(_library)

        self.libraries.add(_library)

    def has_files(self):

        return self.testfolders.has_files() or len(self.testsuites) != 0 or len(self.resources) != 0

    def validate(self):

        self.model.valid = True

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

    def __init__(self,parent,main_ctrl,path,logger):

        _SCR_Control_Base.__init__(
                                    self,
                                    path=path,
                                    name=os.path.splitext(os.path.split(path)[1])[0],
                                    folder=os.path.split(path)[0],
                                    parent=parent,
                                    main_ctrl=main_ctrl,
                                    model=SCR_Model_TestSuite(),
                                    ctrl_type="Test Suite",
                                    logger=logger)

        self.testcases   = SCR_Control_TestCases()
        self.keywords    = SCR_Control_Keywords()
        self.variables   = SCR_Control_Variables()        
        self.resources   = SCR_Control_Resources()
        self.libraries   = SCR_Control_Libraries()

    def read(self,observer):

        self.logger.debug("reading test suite [{}]".format(self.path))

        _status = False

        if None != observer:

            observer.message("reading test suite {}".format(self.name,))

        if os.path.exists(self.path):

            self.model.read_rf_model(self.path)

            self.main_ctrl.testsuites.add(self)

            self.read_resources(observer)

            self.read_libraries(observer)

            self.read_variables(observer)

            self.read_keywords(observer)

            self.read_testcases(observer)

            _status = True
        else:
            self.logger.error("test suite path does not exist [{}]".format(self.path))

        return _status

    def read_resources(self,observer):

        for _name,_model in self.model.get_resources_rf_models():

            _path = os.path.abspath(os.path.join(self.folder,_name))

            _resource = self.main_ctrl.resources.find_by_attribute("path",_path)

            if _resource == None:

                _resource = SCR_Control_Resource(
                                                    parent=self,
                                                    main_ctrl=self.main_ctrl,
                                                    path=_path,
                                                    logger=self.logger)

                _resource.read(observer)

                self.main_ctrl.resources.add(_resource)

    def read_libraries(self,observer):

        for _name,_model in self.model.get_libraries_rf_models():

            _path = os.path.abspath(os.path.join(self.folder,_name))

            if os.path.exists(_path):

                _library = self.main_ctrl.libraries.find_by_attribute("path",_path)

                if _library == None:

                    _library = SCR_Control_Library(
                                                    parent=self,
                                                    main_ctrl=self.main_ctrl,
                                                    path=_path,
                                                    logger=self.logger)

                    _library.read(observer)

                    self.main_ctrl.libraries.add(_library)
            else:
                self.logger.error("libraries path does not exist [{}]".format(_path))

    def read_variables(self,observer):

        for _name,_model in self.model.get_variables_rf_models():

            _ctrl = SCR_Control_Variable(
                                            parent=self,
                                            main_ctrl=self.main_ctrl,
                                            path=self.path,
                                            name=_name,
                                            logger=self.logger)

            _ctrl.read(observer)

            _ctrl.model.load_rf_model(_model)

    def read_keywords(self,observer):

        for _name,_model in self.model.get_keywords_rf_models():

            _ctrl = SCR_Control_Keyword(
                                            parent=self,
                                            main_ctrl=self.main_ctrl,
                                            path=self.path,
                                            name=_name,
                                            logger=self.logger)

            _ctrl.read(observer)

            _ctrl.model.load_rf_model(_model)

    def read_testcases(self,observer):

        for _name,_model in self.model.get_testcases_rf_models():

            _ctrl = SCR_Control_TestCase(
                                            parent=self,
                                            main_ctrl=self.main_ctrl,
                                            path=self.path,
                                            name=_name,
                                            logger=self.logger)

            _ctrl.read(observer)

            _ctrl.model.load_rf_model(_model)

    def validate(self):

        self.model.valid = True

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

    def __init__(self,parent,main_ctrl,path,logger):

        _SCR_Control_Base.__init__(
                                    self,
                                    path=path,
                                    name=os.path.splitext(os.path.split(path)[1])[0],
                                    folder=os.path.split(path)[0],
                                    parent=parent,
                                    main_ctrl=main_ctrl,
                                    model=SCR_Model_Resource(),
                                    ctrl_type="Test Resource",
                                    logger=logger)

        self.keywords    = SCR_Control_Keywords()
        self.variables   = SCR_Control_Variables()
        
        self.resources   = SCR_Control_Resources()
        self.libraries   = SCR_Control_Libraries()

        self.external = not os.path.abspath(path).startswith(os.path.abspath(main_ctrl.testfolder.path))

    def read(self,observer):

        self.logger.debug("reading resource [{}]".format(self.path))

        _status = False

        if None != observer:

            observer.message("reading resource {}".format(self.name,))

        if os.path.exists(self.path):

            self.model.read_rf_model(self.path)

            self.read_resources(observer)

            self.read_libraries(observer)

            self.read_variables(observer)

            self.read_keywords(observer)

            _status = True
        else:
            self.logger.error("resource path does not exist [{}]".format(self.path))

        return _status

    def read_resources(self,observer):

        for _name,_model in self.model.get_resources_rf_models():

            _path = os.path.abspath(os.path.join(self.folder,_name))

            _resource = self.main_ctrl.resources.find_by_attribute("path",_path)

            if _resource == None:

                _resource = SCR_Control_Resource(
                                                    parent=self,
                                                    main_ctrl=self.main_ctrl,
                                                    path=_path,
                                                    logger=self.logger)

                _resource.read(observer)

                self.main_ctrl.resources.add(_resource)

    def read_libraries(self,observer):

        for _name,_model in self.model.get_libraries_rf_models():

            _path = os.path.abspath(os.path.join(self.folder,_name))

            if os.path.exists(_path):

                _library = self.main_ctrl.libraries.find_by_attribute("path",_path)

                if _library == None:

                    _library = SCR_Control_Library(
                                                    parent=self,
                                                    main_ctrl=self.main_ctrl,
                                                    path=_path,
                                                    logger=self.logger)

                    _library.read(observer)

                    self.main_ctrl.libraries.add(_library)
            else:
                self.logger.error("libraries path does not exist [{}]".format(_path))

    def read_variables(self,observer):

        for _name,_model in self.model.get_variables_rf_models():

            _ctrl = SCR_Control_Variable(
                                            parent=self,
                                            main_ctrl=self.main_ctrl,
                                            path=self.path,
                                            name=_name,
                                            logger=self.logger)

            _ctrl.read(observer)

            _ctrl.model.load_rf_model(_model)

    def read_keywords(self,observer):

        for _name,_model in self.model.get_keywords_rf_models():

            _ctrl = SCR_Control_Keyword(
                                            parent=self,
                                            main_ctrl=self.main_ctrl,
                                            path=self.path,
                                            name=_name,
                                            logger=self.logger)

            _ctrl.read(observer)

            _ctrl.model.load_rf_model(_model)

    def validate(self):

        self.model.valid = True

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

    def __init__(self,parent,main_ctrl,path,logger):

        _SCR_Control_Base.__init__(
                                    self,
                                    path=path,
                                    name=os.path.splitext(os.path.split(path)[1])[0],
                                    folder=os.path.split(path)[0],
                                    parent=parent,
                                    main_ctrl=main_ctrl,
                                    model=SCR_Model_Library(),
                                    ctrl_type="Test Library",
                                    logger=logger)

        self.external = not os.path.abspath(path).startswith(os.path.abspath(main_ctrl.testfolder.path))

    def read(self,observer):

        self.logger.debug("reading library [{}]".format(self.path))

        if None != observer:

            observer.message("reading library {}".format(self.name,))

    def validate(self):

        self.model.valid = True

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control_TestCases(SCR_Base_List):

    def __init__(self):

        SCR_Base_List.__init__(self)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control_TestCase(_SCR_Control_WitTable):

    def __init__(self,parent,main_ctrl,path,name,logger):

        _SCR_Control_WitTable.__init__(
                                        self,
                                        path=path,
                                        name=name,
                                        folder=os.path.split(path)[0],
                                        parent=parent,
                                        main_ctrl=main_ctrl,
                                        model=SCR_Model_TestCase(),
                                        ctrl_type="TestCase",
                                        logger=logger)

    def read(self,observer):

        #add the testcase controller to the scrib main controller list of testcase controllers
        self.main_ctrl.testcases.add(self)

        #add the testcase controller to the parent suite list of testcase controllers
        self.parent.testcases.add(self)

        #search in the suite rf models to find the rf model of this test case
        #once found load the testcase rf model in the scrib testcase model
        for _rf_model_name,_rf_model in self.parent.model.get_testcases_rf_models():

            if self.name == _rf_model_name:

                self.model.load_rf_model(_rf_model)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control_Variables(SCR_Base_List):

    def __init__(self):

        SCR_Base_List.__init__(self)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control_Variable(_SCR_Control_Base):

    def __init__(self,parent,main_ctrl,path,name,logger):

        _SCR_Control_Base.__init__(
                                    self,
                                    path=path,
                                    name=name,
                                    folder=os.path.split(path)[0],
                                    parent=parent,
                                    main_ctrl=main_ctrl,
                                    model=SCR_Model_Variable(),
                                    ctrl_type="Variable",
                                    logger=logger)

    def read(self,observer):

        self.main_ctrl.variables.add(self)

        self.parent.variables.add(self)

    def validate(self):

        self.model.valid = True

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control_Keywords(SCR_Base_List):

    def __init__(self):

        SCR_Base_List.__init__(self)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Control_Keyword(_SCR_Control_WitTable):

    def __init__(self,parent,main_ctrl,path,name,logger):

        _SCR_Control_WitTable.__init__(
                                        self,
                                        path=path,
                                        name=name,
                                        folder=os.path.split(path)[0],
                                        parent=parent,
                                        main_ctrl=main_ctrl,
                                        model=SCR_Model_Keyword(),
                                        ctrl_type="Keyword",
                                        logger=logger)

    def read(self,observer):

        self.main_ctrl.keywords.add(self)

        self.parent.keywords.add(self)
