import os

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
def scr_get_settings_dir():

    _path = os.path.join(os.path.expanduser("~"),".scrib")

    if not os.path.exists(_path):
        
        os.mkdir(_path)  
        
    return _path

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
def scr_get_logger_dir():

    _path = scr_get_settings_dir()

    _path = os.path.join(_path,"log")

    if not os.path.exists(_path):
        
        os.mkdir(_path)  
        
    return _path

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
def get_all_folders(path):

    _folders = []
    
    for _dirpath, _dirnames, _filenames in os.walk(path):

        _folders.append(_dirpath)
        
    return _folders

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
def get_all_files(path,extensions):

    _files = []
    
    for _dirpath, _dirnames, _filenames in os.walk(path):

        for _file in _filenames:

            if extensions == None:

                _files.append(os.path.join(_dirpath,_file))

            else:
                if os.path.splitext(_file)[1] in extensions:

                    _files.append(os.path.join(_dirpath,_file))
        
    return _files

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_UtilProgress():
    """
    Class used when tracking progress for progress bar
    The class will be used to instantiate an imutble object 
    that can be used in recursive calls
    """

    def __init__(self,nr_of_items):

        self.count       = 0 
        self.nr_of_items = nr_of_items

    def increment(self):

        self.count += 1

    def get_progress(self):

        if self.nr_of_items > 0:
            _progress = int((float(self.count) / float(self.nr_of_items)) * 100.0)
        else:
            _progress = 0

        return _progress

    def get_progress_text(self):

        return ("[{}/{}][{}]".format(self.count,self.nr_of_items,self.get_progress()))
