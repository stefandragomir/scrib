
from PyQt5.QtCore          import *
from PyQt5.QtGui           import *
from PyQt5.QtWidgets       import * 
from icons.icons           import SCR_GetIcon
from widgets.widgets       import SCR_WDG_Tree
from widgets.widgets       import SCR_WDG_Tree_Model

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_TestTree_Model(SCR_WDG_Tree_Model):

	def __init__(self,parent):

		SCR_WDG_Tree_Model.__init__(self,parent)

	def load(self,data):

		pass

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_WDG_TestTree(SCR_WDG_Tree):

	def __init__(self, config):

		SCR_WDG_Tree.__init__(
								self,
								config=config, 
								usefind=True,
								with_metadata=True,
								model_class=SCR_WDG_TestTree_Model)
