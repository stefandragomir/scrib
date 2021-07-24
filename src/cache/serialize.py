import os
import pickle
import gzip

from datetime          import datetime
from config.config     import SCR_VERSION


"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_Serialiser(object):

    def __init__(self,path):

    	self.path = path

    def __serialise(self,data):

        _data = {
                        "data"     :data,
                        "timestamp":datetime.now(),
                        "version"  :SCR_VERSION
                }

        _serial_data = pickle.dumps(_data)

        return _serial_data

    def __deserialise(self,serial_data):

        try:
            _data = pickle.loads(serial_data)
        except:
            _data = {"data":None,"timestamp":None,"version":"0.0.0"}

        return _data

    def __compress(self,serial_data):

        _file_stream = gzip.open(self.path, 'wb')

        _file_stream.write(serial_data)

        _file_stream.close()

    def __decompress(self):

        _file_stream = gzip.open(self.path, 'rb')

        _data = _file_stream.read()

        _file_stream.close()

        return _data

    def get_data(self):

        if os.path.exists(self.path):

            _serial_data = self.__decompress()

            _data = self.__deserialise(_serial_data)
        else:
            _data = {"data":None,"timestamp":None,"version":"0.0.0"}

        if "data" not in _data.keys():
            _data.update({"data":None})

        if "timestamp" not in _data.keys():
            _data.update({"timestamp":None})

        if "version" not in _data.keys():
            _data.update({"version":"0.0.0"})

        return _data

    def set_data(self,data):

        _serial_data = self.__serialise(data)

        self.__compress(_serial_data)
