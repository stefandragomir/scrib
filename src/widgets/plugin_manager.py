"""
File contains all classes for loading and managing plugins
"""

import os
import importlib
import inspect

from widgets.widgets       import SCR_WDG_Widget
from widgets.widgets       import SCR_WDG_PopUp
from messenger.messenger   import SCR_Messenger
from abc                   import abstractmethod
from utils.utils           import get_plugins_path
from model.model           import SCR_Base_List

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_PluginManager():

    def __init__(self,config,logger,preferences):

        self.logger      = logger
        self.config      = config
        self.plugins     = SCR_Base_List()
        self.preferences = preferences

    def load_plugins(self):

        _paths_plugins = self.find_plugins_paths()

        for _path in _paths_plugins:

            self.find_plugin_classes(_path)

        for _plugin in self.plugins:

            _plugin.instance = _plugin.object(
                                                self.config,
                                                self.logger,
                                                self.preferences)

    def find_plugins_paths(self):

        _paths = []

        _path_plugins = get_plugins_path()

        if os.path.exists(_path_plugins):

            for _path in os.listdir(_path_plugins):            

                _path = os.path.join(_path_plugins,_path)

                if os.path.isdir(_path):

                    _path_plugin = os.path.join(_path,"plugin.py")

                    if os.path.exists(_path_plugin):

                        self.logger.debug("found plugin.py in folder [{}]".format(_path))

                        _paths.append(_path_plugin)
        else:
            self.logger.error("could not find plugins path [{}]".format(_path_plugins))            

        return _paths

    def find_plugin_classes(self,module_path):

        _module_name    = os.path.splitext(os.path.basename(module_path))[0]
        
        try:

            _spec = importlib.util.spec_from_file_location(_module_name, module_path)

            if _spec is not None:
                
                _module = importlib.util.module_from_spec(_spec)

                _spec.loader.exec_module(_module)

                try:
                    
                    for _name, _obj in inspect.getmembers(_module):

                        if inspect.isclass(_obj):

                            if issubclass(_obj, SCR_Plugin) and SCR_Plugin != _obj:

                                _plugin = SCR_PluginContainer()

                                _plugin.name   = _name
                                _plugin.object = _obj

                                self.plugins.add(_plugin)
                except:
                    self.logger.error("could not inspect plugin file [{}]".format(module_path)) 

        except Exception as _exception:
            
            self.logger.error("could not load plugin file [{}]".format(module_path))
            self.logger.error("exception [{}]".format(_exception))

            SCR_WDG_PopUp(
                            self.config,
                            "Error Loading Plugin",
                            "Error loading plugin [{}] [{}]".format(module_path,_exception))

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_PluginContainer():

    def __init__(self):

        self.name     = ""
        self.object   = None
        self.instance = None

    def __repr__(self):

        return self.__print()

    def __str__(self):

        return self.__print()

    def __print(self):
        
        _txt = "Plugin [{}] [{}] [{}]".format(self.name, self.object, self.instance)

        return _txt

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_Plugin(SCR_WDG_Widget):

    def __init__(self,name,author,version,config,logger,preferences):

        SCR_WDG_Widget.__init__(self,config)

        self.name        = name
        self.author      = author
        self.version     = version
        self.messenger   = SCR_Messenger()
        self.logger      = logger
        self.preferences = preferences

    @abstractmethod
    def load(self):

        raise NotImplementedError

    @abstractmethod
    def unload(self):

        raise NotImplementedError