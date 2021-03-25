import os
import zipfile

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_Logger(object):

    __LOG_LEVEL_DEBUG = "DEBUG"
    __LOG_LEVEL_INFO  = "INFO" 
    __LOG_LEVEL_ERROR = "ERROR"

    def __init__(self, debug=False, path=None, ui=None):

        self.__debug_level  = debug
        self.__path         = path
        self.__ui           = ui

    def __log_to_file(self,txt):

        if self.__path:

            if not os.path.exists(self.__path):

                with open(self.__path,'w+',encoding='utf-8') as _log:
                    _log.write(" ")

            if self.__is_log_to_big():

                self.__archive_log()

            with open(self.__path, 'a', encoding='utf-8') as _log_file:

                _log_file.write(txt)

    def __log_to_ui(self,txt):

        if self.__ui:

            self.__ui.write(txt)

    def __archive_log(self):

        _archive_path = os.path.join(os.path.split(self.__path)[0],"scrib_log_archive")
        
        if not os.path.exists(_archive_path):
            os.makedirs(_archive_path)

        _archive_path = os.path.join(_archive_path,strftime("scrib_log_%d_%m_%Y_%H_%M_%S.zip", gmtime()))

        _arch = zipfile.ZipFile(_archive_path, mode='w')

        _arch.write(
                    self.__path,
                    os.path.basename(self.__path), 
                    compress_type=zipfile.ZIP_DEFLATED)

        _arch.close()

        os.remove(self.__path)

    def __log(self,txt,level):

        _date    = datetime.now().strftime("%I:%M:%S %p %d-%B-%Y")

        _log_txt = "[%s] %s -> %s" % (_date, level, txt)

        self.__log_to_file(_log_txt + "\n")

        self.__log_to_ui(_log_txt + "\n")

    def __is_log_to_big(self):

        return os.path.getsize(self.__path) >= 10000000

    def info(self, txt):

        self.__log(txt,self.__LOG_LEVEL_INFO)

    def error(self, txt):

        self.__log(txt,self.__LOG_LEVEL_ERROR)

    def debug(self, txt):

        if self.__debug_level:

            self.__log(txt,self.__LOG_LEVEL_DEBUG)
