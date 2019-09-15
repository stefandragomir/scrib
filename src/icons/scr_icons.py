import os, sys
import itertools

from icons.scr_icons_db   import SCR_Icons
from icons.scr_icons_db_1 import SCR_ICONS_db1
from icons.scr_icons_db_2 import SCR_ICONS_db2
from icons.scr_icons_db_3 import SCR_ICONS_db3
from icons.scr_icons_db_4 import SCR_ICONS_db4

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
def SCR_GetIcon(name):

    _icon = SCR_ICONS_db1[name]
    if not _icon:
        _icon = SCR_ICONS_db2[name]
        if not _icon:
            _icon = SCR_ICONS_db3[name]
            if not _icon:
                _icon = SCR_ICONS_db4[name]

    return _icon.as_icon()

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
def SCR_GetPixmap(name):

    _icon = SCR_ICONS_db1[name]
    if not _icon:
        _icon = SCR_ICONS_db2[name]
        if not _icon:
            _icon = SCR_ICONS_db3[name]
            if not _icon:
                _icon = SCR_ICONS_db4[name]

    return _icon.as_pixmap()

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
def SCR_GetByteArray(name):

    _icon = SCR_ICONS_db1[name]
    if not _icon:
        _icon = SCR_ICONS_db2[name]
        if not _icon:
            _icon = SCR_ICONS_db3[name]
            if not _icon:
                _icon = SCR_ICONS_db4[name]

    return _icon.as_bytearray()

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
def SCR_GetIconNames():

    _icons_name = []

    for _icon in itertools.chain(SCR_ICONS_db1, SCR_ICONS_db2, SCR_ICONS_db3, SCR_ICONS_db4):
    	_icons_name.append(_icon.name)
        
    return _icons_name
