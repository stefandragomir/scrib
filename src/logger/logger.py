import os
import zipfile
from datetime import datetime

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_Logger(object):

    LOG_LEVEL_DEBUG = "DEBUG"
    LOG_LEVEL_INFO  = "INFO" 
    LOG_LEVEL_ERROR = "ERROR"

    def __init__(self):

        self.debug_level  = False
        self.path         = None
        self.ui           = None
        self.max_log_size = 10000000

    def __log_to_file(self,txt):

        if self.path:

            if not os.path.exists(self.path):

                with open(self.path,'w+',encoding='utf-8') as _log:
                    _log.write(" ")

            if self.__is_log_to_big():

                self.__archive_log()

            with open(self.path, 'a', encoding='utf-8') as _log_file:

                _log_file.write(txt)

    def __log_to_ui(self,txt):

        if self.ui != None:

            self.ui.write(txt)

    def __archive_log(self):

        _archive_path = os.path.join(os.path.split(self.path)[0],"scrib_log_archive")
        
        if not os.path.exists(_archive_path):
            os.makedirs(_archive_path)

        _archive_path = os.path.join(_archive_path,strftime("scrib_log_%d_%m_%Y_%H_%M_%S.zip", gmtime()))

        _arch = zipfile.ZipFile(_archive_path, mode='w')

        _arch.write(
                    self.path,
                    os.path.basename(self.path), 
                    compress_type=zipfile.ZIP_DEFLATED)

        _arch.close()

        os.remove(self.path)

    def __log(self,txt,level):

        _date    = datetime.now().strftime("%I:%M:%S %p %d-%B-%Y")

        _log_txt = "[%s] %s -> %s" % (_date, level, txt)

        self.__log_to_file(_log_txt + "\n")

        self.__log_to_ui(_log_txt)

    def __is_log_to_big(self):

        return os.path.getsize(self.path) >= self.max_log_size

    def info(self, txt):

        self.__log(txt,self.LOG_LEVEL_INFO)

    def error(self, txt):

        self.__log(txt,self.LOG_LEVEL_ERROR)

    def debug(self, txt):

        if self.debug_level:

            self.__log(txt,self.LOG_LEVEL_DEBUG)


    def set_debug_level(self,state):

        self.debug_level = state

    def set_path(self,path):

        self.path = path

    def set_ui(self,ui):

        self.ui = ui
