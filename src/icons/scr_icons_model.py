from PyQt5.QtCore                  import QByteArray
from PyQt5.QtGui                   import QPixmap
from PyQt5.QtGui                   import QIcon

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Icon(object):

    def __init__(self):

        self.name       = ""
        self.img        = ""

    def as_icon(self):

        _icon = None

        _barray = QByteArray()
        _barray_data = _barray.fromBase64(self.img.encode("utf-8"))

        #create pixmap from base64 data
        _pixmap = QPixmap ()
        _pixmap.loadFromData(_barray_data, "PNG")

        #create icon
        _icon  = QIcon()
        _icon.addPixmap(_pixmap)

        return _icon

    def as_pixmap(self):

        _pixmap = None

        _barray = QByteArray()
        _barray_data = _barray.fromBase64(self.img.encode("utf-8"))

        #create pixmap from base64 data
        _pixmap = QPixmap ()
        _pixmap.loadFromData(_barray_data, "PNG")

        return _pixmap

    def as_bytearray(self):

        _barray_data = None

        _barray = QByteArray()
        _barray_data = _barray.fromBase64(self.img.encode("utf-8"))

        return _barray_data

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Icons(object):

    def __init__(self):

        self.icons = []

    def add(self,obj):

        self.icons.append(obj)  

    def __repr__(self):

        return self.__print()

    def __str__(self):

        return self.__print()

    def __print(self):

        _txt = ""
        
        for _icon in self.icons:

            _txt += str(_icon.name) + "\n"

        return _txt

    def __iter__(self):

        for _icon in self.icons:

            yield _icon

    def __getitem__(self,name):

        return self.find_by_attribute("name",name)

    def __len__(self):

        return len(self.icons)

    def __contains__(self,obj):

        return _local_icon.name in [_local_icon.name for _local_icon in self.icons]

    def find_by_attribute(self,attribute,value):

        _return_icon = None

        for _icon in self.icons:

            if getattr(_icon,attribute) == value:

                _return_icon = _icon

        return _return_icon

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
