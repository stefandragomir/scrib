import os
import sys
import itertools
import sqlite3

from PyQt5.QtGui    import QIcon
from PyQt5.QtGui    import QPixmap
from PyQt5.QtCore   import QByteArray

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
SCR_BUFFER_ICON = {}

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
def SCR_Icons_Get_DB():

    _path = os.path.abspath(__file__)
    _path = os.path.split(_path)[0]
    _path = os.path.join(_path,"icons.db")

    if not os.path.exists(_path):

        _path = os.path.abspath(__file__)
        _path = os.path.split(_path)[0]
        _path = os.path.split(_path)[0]
        _path = os.path.split(_path)[0]
        _path = os.path.join(_path,"icons.db")

    _db = SCR_Database(_path)

    return _db
    
"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
def SCR_As_Icon(base64_data):

    _barray = QByteArray()

    _barray_data = _barray.fromBase64(base64_data.encode("utf-8"))

    _pixmap = QPixmap ()

    _pixmap.loadFromData(_barray_data, "PNG")

    _icon  = QIcon()

    _icon.addPixmap(_pixmap)
    
    return _icon

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
def SCR_As_Pixmap(base64_data):

    _barray = QByteArray()

    _barray_data = _barray.fromBase64(base64_data.encode("utf-8"))

    _pixmap = QPixmap ()

    _pixmap.loadFromData(_barray_data, "PNG")
    
    return _pixmap

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
def SCR_As_ByteArray(base64_data):

    _barray = QByteArray()

    _barray_data = _barray.fromBase64(basbase64_datae64String.encode("utf-8"))

    return _barray_data

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
def SCR_Buffer_Add_Icon(name,size):

    global SCR_BUFFER_ICON

    SCR_BUFFER_ICON.update({name: SWTW_GetIcon(name,size=size)})

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
def SCR_GetIcon(name,size="medium"):

    global SCR_BUFFER_ICON

    _icon = QIcon()

    if name in list(SCR_BUFFER_ICON.keys()):
        _icon = SCR_BUFFER_ICON[name]
    else:
        
        _db  = SCR_Icons_Get_DB()

        _base64_data = _db.get_icon(name,size)

        if _base64_data:

            _icon = SCR_As_Icon(_base64_data)

    return _icon

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
def SCR_GetPixmap(name,size="medium"):

    _icon = QPixmap()

    _db  = SCR_Icons_Get_DB()

    _base64_data = _db.get_icon(name,size)

    if _base64_data:

        _icon = SCR_As_Pixmap(_base64_data)

    return _icon

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
def SCR_GetByteArray(name,size="medium"):

    data = QByteArray()

    _db  = SCR_Icons_Get_DB()

    _base64_data = _db.get_icon(name,size)

    if _base64_data:

        data = SCR_As_ByteArray(_base64_data)

    return data

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
def SCR_GetIconNames():

    _db          = SCR_Icons_Get_DB()

    _icons_name  = _db.get_names()
        
    return _icons_name

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Database():

    def __init__(self,path):

        self.path      = path
        
    def connect(self):

        try:
            self.hdl = sqlite3.connect(self.path)
        except sqlite3.Error as e:
            print(e)        

    def get_all_table_rows(self):

        self.connect()

        _records = []

        _cursor = self.hdl.cursor()

        try:
            _cursor.execute("""SELECT * from Images""")
        except sqlite3.Error as e:
            print(e)

        _records = _cursor.fetchall()

        self.close()

        return _records     

    def get_names(self):

        return [record[1] for record in self.get_all_table_rows()]

    def get_icon(self,name,size):

        self.connect()

        _data = ''

        _cursor = self.hdl.cursor()

        try:
            _cursor.execute("""SELECT * from Images WHERE name = '%s'""" % (name,))
        except sqlite3.Error as e:
            print(e)

        _record = _cursor.fetchall()[0]
            
        if size == "small":

            _data = _record[3]

        elif size == "medium":

            _data = _record[4]

        elif size == "large":

            _data = _record[5]

        self.close()

        return _data

    def get_row_by_name(self,name):

        self.connect()

        _record = []

        _cursor = self.hdl.cursor()

        try:
            _cursor.execute("""SELECT * from Images WHERE name = '%s'""" % (name,))
        except sqlite3.Error as e:
            print(e)
        else:
            _record = _cursor.fetchall()[0]
                
        return _record

    def insert(self,element):

        self.connect()

        try:
            self.hdl.cursor().execute(
                                        "INSERT INTO Images (name,tags,img_small,img_medium,img_large) VALUES(?,?,?,?,?) ",
                                        [
                                            str(element['name']),
                                            str(element['tags']),
                                            str(element['img_small']),
                                            str(element['img_medium']),
                                            str(element['img_large'])
                                        ]
                                    )
        except sqlite3.Error as e:
            print(e)

        self.hdl.commit()

        self.close()

    def delete_row_by_name(self,name):

        self.connect()

        try:
            self.hdl.cursor().execute("DELETE FROM Images WHERE name = ?",(name,))
        except sqlite3.Error as e:
            print(e)

        self.hdl.commit()

        self.close()

    def close(self):

        self.hdl.close()
