
from abc                              import abstractmethod
from robot.api                        import get_tokens
from robot.api                        import get_model
from robot.parsing.model.blocks       import TestCaseSection
from robot.parsing.model.blocks       import VariableSection
from robot.parsing.model.blocks       import KeywordSection
from robot.parsing.model.blocks       import SettingSection
from robot.parsing.model.blocks       import Keyword
from robot.parsing.model.blocks       import ValidationContext
from robot.parsing.model.statements   import Variable
from robot.parsing.model.statements   import ResourceImport
from robot.parsing.model.statements   import LibraryImport
from robot.parsing.model.statements   import Documentation
from robot.parsing.model.statements   import KeywordCall
from robot.parsing.model.statements   import EmptyLine
from robot.parsing.model.statements   import Tags
from robot.parsing.model.statements   import Comment

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
class SCR_Model_Error():

    ERROR_OK              = 0
    ERROR_UNKNOWN_KEYWORD = 1

    def __init__(self):

        self.row    = 0
        self.column = 0
        self.number = 0
        self.text   = ""

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class _SCR_Model_Base_Item():

    def __init__(self):

        self.rf_model   = None
        self.valid      = True
        self.errors     = SCR_Base_List()
        self._error_map = {

                            SCR_Model_Error.ERROR_UNKNOWN_KEYWORD: 'Keyword "{}" cannot be found in any Test Suite, Resource or Library',


                          }

    def add_error(self,row,column,number,*args):

        _error        = SCR_Model_Error()
        _error.line   = row
        _error.column = column
        _error.number = number
        _error.text   = self._error_map[number].format(*args)

        self.errors.add(_error)

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
class _SCR_Model_WithStatements():
    """
    Used by models that contain statements (calls, assignments)
    Used for Test Cases and Keywords
    """

    def __init__(self):

        #map of statement types to methods that return 
        #the number of cells ocupied by the statement
        self._map_size = {
                                EmptyLine     : self.get_statement_empty_line_size,
                                KeywordCall   : self.get_statement_keyword_call_size,
                                Documentation : self.get_statement_documentation_size,
                                Tags          : self.get_statement_tags_size,
                                Comment       : self.get_statement_comment_size,
                        }

    def is_statement_keyword_call(self,statement):

        return type(statement) == KeywordCall

    def get_statement_keyword_name(self,statement):

        return statement.tokens[len(statement.assign) + 1].value

    def get_statement_visible_tokens(self,statement):
        """
        Method receives a rf statement and returns tokens that should be visible to the user
        Returns token that are not space separators of end of line
        """

        _non_functional_tokens = [
                                    Token.SEPARATOR,
                                    Token.EOL,
                                    Token.EOS]

        return [_token for _token in statement.tokens if _token.type not in _non_functional_tokens]

    def get_statements(self):
        """
        Method returns a list of all statements in the model
        """

        return self.rf_model.body

    def get_statement_by_index(self,index):
        """
        Method returns the statement positioned at an index in the model
        """

        return self.rf_model.body[index]

    def get_statement_text_by_index(self,index):
        """
        Return the entire text of a statement
        Each relevant token will be placed the list
        Method does not return text control tokens (spaces, end of lines, etc)
        """

        _text = [_token.value for _token in self.get_statement_visible_tokens(self.rf_model.body[index])]

        return _text

    def get_nr_of_statements(self):
        """
        Return the number of statements in the model without the last one
        Last statement is End Of File
        """

        return len(self.rf_model.body) - 1

    def get_max_statement_size(self):
        """
        Get the maximum number of cells used in any statement in the model
        Used to determine the number of columns needed in the editor grid
        """

        #depending on the type of the statement, the maximum number of cells is returned
        _size = max(self._map_size[type(_statement)](_statement) for _statement in self.rf_model.body)

        return _size

    def get_statement_size(self,statement):
        """
        Get the number of cells used in any statement in the model
        Used to determine the number of columns needed in the editor grid
        """

        return self._map_size[type(statement)](statement)

    def get_statement_keyword_call_size(self,statement):
        """
        Method returns the number of cells used by a keyword call statement
        """

        #add one for the keyword call
        _statement_size = 1

        #add the number of assignments
        _statement_size += len(statement.assign)

        #add the number of arguments
        _statement_size += len(statement.args)

        return _statement_size

    def get_statement_empty_line_size(self,statement):
        """
        Method returns the number of cells used by an empty statement
        """

        return 0

    def get_statement_documentation_size(self,statement):

        return 0

    def get_statement_tags_size(self,statement):

        return 0

    def get_statement_comment_size(self,statement):

        _statement_size = len(self.get_statement_visible_tokens(statement))

        return _statement_size

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Model_Folder(_SCR_Model_Base_Item):

    def __init__(self):

        _SCR_Model_Base_Item.__init__(self)

    def load_rf_model(self,rf_model):

        self.rf_model = rf_model

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Model_TestSuite(_SCR_Model_Base_Item):

    def __init__(self):

        _SCR_Model_Base_Item.__init__(self)

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
class SCR_Model_Resource(_SCR_Model_Base_Item):

    def __init__(self):

        _SCR_Model_Base_Item.__init__(self)

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
class SCR_Model_TestCase(_SCR_Model_Base_Item,_SCR_Model_WithStatements):

    def __init__(self):

        _SCR_Model_Base_Item.__init__(self)

        _SCR_Model_WithStatements.__init__(self)

    def load_rf_model(self,rf_model):

        self.rf_model = rf_model

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Model_Variable(_SCR_Model_Base_Item):

    def __init__(self):

        _SCR_Model_Base_Item.__init__(self)

    def load_rf_model(self,rf_model):

        self.rf_model = rf_model

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Model_Keyword(_SCR_Model_Base_Item,_SCR_Model_WithStatements):

    def __init__(self):

        _SCR_Model_Base_Item.__init__(self)

        _SCR_Model_WithStatements.__init__(self)

    def load_rf_model(self,rf_model):

        self.rf_model = rf_model

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Model_Library(_SCR_Model_Base_Item):

    def __init__(self):

        _SCR_Model_Base_Item.__init__(self)

    def load_rf_model(self,rf_model):

        self.rf_model = rf_model
