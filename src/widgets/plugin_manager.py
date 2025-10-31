"""
File contains all classes for loading and managing plugins
"""

from widgets.widgets       import SCR_WDG_Widget
from messenger.messenger   import SCR_Messenger
from abc                   import abstractmethod

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_PluginManager():

    def __init__(self,logger):

        pass

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_Plugin(SCR_WDG_Widget):

    def __init__(self,name,author,version,config,logger,preferences):

        SCR_WDG_Widget.__init__(config)

        self.name        = name
        self.author      = author
        self.version     = version
        self.messenger   = SCR_Messenger()
        self.logger      = logger
        self.preferences = preferences

    @abstractmethod
    def load(self):

        pass

    @abstractmethod
    def unload(self):

        pass