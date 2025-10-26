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

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Base_List(object):

    def __init__(self):

        self.objects = []

    def add(self,obj):

        self.objects.append(obj)  

    def remove(self,obj):

        self.objects.remove(obj)  

    def remove_by_attribute(self,attribute,value):

        _item = self.find_by_attribute(attribute,value)

        if _item != None:

            self.remove(_item)

    def __repr__(self):

        return self.__print()

    def __str__(self):

        return self.__print()

    def __print(self):

        _txt = ""
        
        for obj in self.objects:

            _txt += str(obj)

        return _txt

    def __iter__(self):

        for obj in self.objects:

            yield obj

    def __getitem__(self,index):

        return self.objects[index]

    def __len__(self):

        return len(self.objects)

    def find_by_attribute(self,attribute,value):

        _object = None

        for _obj in self.objects:

            if getattr(_obj,attribute) == value:

                _object = _obj

        return _object

    def __add__(self,other):

        self.objects += other.objects

        return self

    def reverse(self):

        self.objects.reverse()

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Model_Base_Item(object):

    def __init__(self):

        self.rf_model = None

    @abstractmethod
    def load_rf_model(self,rf_model):

        raise NotImplementedError

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

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Model_Folder(SCR_Model_Base_Item):

    def __init__(self):

        SCR_Model_Base_Item.__init__(self)

    def load_rf_model(self,rf_model):

        self.rf_model = rf_model

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Model_TestSuite(SCR_Model_Base_Item):

    def __init__(self):

        SCR_Model_Base_Item.__init__(self)

    def load_rf_model(self,rf_model):

        self.rf_model = rf_model

    def get_sections(self):

        return self.rf_model.sections

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Model_Resource(SCR_Model_Base_Item):

    def __init__(self):

        SCR_Model_Base_Item.__init__(self)

    def load_rf_model(self,rf_model):

        self.rf_model = rf_model

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Model_TestCase(SCR_Model_Base_Item):

    def __init__(self):

        SCR_Model_Base_Item.__init__(self)

    def load_rf_model(self,rf_model):

        self.rf_model = rf_model

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Model_Variable(SCR_Model_Base_Item):

    def __init__(self):

        SCR_Model_Base_Item.__init__(self)

    def load_rf_model(self,rf_model):

        self.rf_model = rf_model

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Model_Keyword(SCR_Model_Base_Item):

    def __init__(self):

        SCR_Model_Base_Item.__init__(self)

    def load_rf_model(self,rf_model):

        self.rf_model = rf_model

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Model_Library(SCR_Model_Base_Item):

    def __init__(self):

        SCR_Model_Base_Item.__init__(self)

    def load_rf_model(self,rf_model):

        self.rf_model = rf_model
