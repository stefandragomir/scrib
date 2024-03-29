import os
from utils.utils     import scr_get_settings_dir
from cache.serialize import SCR_Serialiser

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_Preferences():

	def __init__(self):

		self.preferences = {
								"recents": [],
								"cwd"    : "",
							}

	def load(self):

		_path = scr_get_settings_dir()

		_path = os.path.join(_path,"preferences.scache")

		_serializer = SCR_Serialiser(_path)

		_data = _serializer.get_data()

		if _data["data"] != None:

			self.preferences = _data["data"]

	def save(self):

		_path = scr_get_settings_dir()

		_path = os.path.join(_path,"preferences.scache")

		_serializer = SCR_Serialiser(_path)

		_data = _serializer.set_data(self.preferences)

	def get(self,name):

		_value = None

		if name in list(self.preferences.keys()):

			_value = self.preferences[name]

		return _value

	def set(self,name,value):

		_value = None

		if name in list(self.preferences.keys()):

			self.preferences[name] = value
