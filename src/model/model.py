
from abc                              import abstractmethod
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
from robot.parsing.model.statements   import KeywordCall
from robot.parsing.model.statements   import EmptyLine
from robot.parsing.lexer.tokens       import Token

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Base_List():

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
class SCR_Model_Base_Item():

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
class SCR_Model_WithStatements():
    """
    Used by models that contain statements (calls, assignments)
    Used for Test Cases and Keywords
    """

    def __init__(self):

        self._map_size = {
                                EmptyLine  :  self.get_statement_empty_line_size,
                                KeywordCall:  self.get_statement_keyword_call_size,
                        }

    def get_statements(self):

        return self.rf_model.body

    def get_statement_by_index(self,index):

        return self.rf_model.body[index]

    def get_statement_text_by_index(self,index):

        _text = []

        for _token in self.rf_model.body[index].tokens:

            if _token.type not in  [Token.SEPARATOR,Token.EOL,Token.EOS]:

                _text.append(_token.value)

        return _text

    def get_nr_of_statements(self):

        return len(self.rf_model.body)

    def get_max_statement_size(self):
        """
        Get the maximum number of operands used in any statement in the model
        Used to determine the number of columns needed in the editor grid
        """

        _size = max(self._map_size[type(_statement)](_statement) for _statement in self.rf_model.body)

        return _size

    def get_statement_size(self,statement):
        """
        Get the number of operands used in any statement in the model
        Used to determine the number of columns needed in the editor grid
        """

        return self._map_size[type(statement)](statement)

    def get_statement_keyword_call_size(self,statement):

        #add one for the keyword call
        _statement_size = 1

        #add the number of assignments
        _statement_size += len(statement.assign)

        #add the number of arguments
        _statement_size += len(statement.args)

        return _statement_size

    def get_statement_empty_line_size(self,statement):

        return 0

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

    def read_rf_model(self,path):

        self.rf_model = get_model(source=path,data_only=False)

    def load_rf_model(self,rf_model):

        self.rf_model = rf_model

    def get_resources_rf_models(self):

        _models = []

        for _section in self.rf_model.sections:

            if self.is_section_settings(_section):

                for _item in _section.body:

                    if self.is_statement_resource_import(_item):

                        _models.append([_item.name,_item])

        return _models

    def get_libraries_rf_models(self):

        _models = []

        for _section in self.rf_model.sections:

            if self.is_section_settings(_section):

                for _item in _section.body:

                    if self.is_statement_library_import(_item):

                        _models.append([_item.name,_item])

        return _models

    def get_variables_rf_models(self):

        _models = []

        for _section in self.rf_model.sections:

            if self.is_section_variables(_section):

                for _item in _section.body:

                    if self.is_statement_variable(_item):

                        _models.append([_item.name,_item])

        return _models

    def get_keywords_rf_models(self):

        _models = []

        for _section in self.rf_model.sections:

            if self.is_section_keywords(_section):

                for _item in _section.body:

                    if self.is_statement_keyword(_item):

                        _models.append([_item.name,_item])

        return _models

    def get_testcases_rf_models(self):

        _models = []

        for _section in self.rf_model.sections:

            if self.is_section_testcases(_section):

                for _item in _section.body:

                    _models.append([_item.name,_item])

        return _models

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Model_Resource(SCR_Model_Base_Item):

    def __init__(self):

        SCR_Model_Base_Item.__init__(self)

    def read_rf_model(self,path):

        self.rf_model = get_model(source=path,data_only=False)

    def load_rf_model(self,rf_model):

        self.rf_model = rf_model

    def get_resources_rf_models(self):

        _models = []

        for _section in self.rf_model.sections:

            if self.is_section_settings(_section):

                for _item in _section.body:

                    if self.is_statement_resource_import(_item):

                        _models.append([_item.name,_item])

        return _models

    def get_libraries_rf_models(self):

        _models = []

        for _section in self.rf_model.sections:

            if self.is_section_settings(_section):

                for _item in _section.body:

                    if self.is_statement_library_import(_item):

                        _models.append([_item.name,_item])

        return _models

    def get_variables_rf_models(self):

        _models = []

        for _section in self.rf_model.sections:

            if self.is_section_variables(_section):

                for _item in _section.body:

                    if self.is_statement_variable(_item):

                        _models.append([_item.name,_item])

        return _models

    def get_keywords_rf_models(self):

        _models = []

        for _section in self.rf_model.sections:

            if self.is_section_keywords(_section):

                for _item in _section.body:

                    if self.is_statement_keyword(_item):

                        _models.append([_item.name,_item])

        return _models

    def get_testcases_rf_models(self):

        _models = []

        for _section in self.rf_model.sections:

            if self.is_section_testcases(_section):

                for _item in _section.body:

                    _models.append([_item.name,_item])

        return _models

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Model_TestCase(SCR_Model_Base_Item,SCR_Model_WithStatements):

    def __init__(self):

        SCR_Model_Base_Item.__init__(self)

        SCR_Model_WithStatements.__init__(self)

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
class SCR_Model_Keyword(SCR_Model_Base_Item,SCR_Model_WithStatements):

    def __init__(self):

        SCR_Model_Base_Item.__init__(self)

        SCR_Model_WithStatements.__init__(self)

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
