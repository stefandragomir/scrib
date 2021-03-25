
import traceback
import os
import yaml
import sys
from widgets.widgets     import SCR_WDG_PopUp
from datetime            import datetime
from config.config       import SCR_VERSION

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Err(object):

    def __init__(self, err_type, err_value, err_traceback):

        self.err_value = str(err_value)
        self.err_type  = str(err_type)
        self.traceback = "\n".join(traceback.format_exception(err_type, err_value, err_traceback))
        self.date      = datetime.now()
        self.path      = ""
        self.version   = SCR_VERSION

    def save(self):

        print(self)

        self.path = "scrib_%s.err" % (datetime.now().strftime("%d_%m_%Y_%I_%M_%S"),)

        _data = {
                    "date"           : str(self.date),
                    "err_type"       : self.err_type,
                    "err_value"      : self.err_value,
                    "version"        : self.version,                    
                    "traceback"      : self.traceback,
                }
                
        self.path = os.path.abspath(self.path)

        with open(self.path, 'w+') as _trans:

            _trans.write( yaml.dump(_data, default_flow_style=False))

        SCR_WDG_PopUp(
                        title="Scrib Error", 
                        txt="Scrib has encountered an error. Please contact development and send them the file %s" % (self.path,), 
                        msgtype="information")

    def __repr__(self):

        return self.__print()

    def __str__(self):

        return self.__print()

    def __print(self):

        _txt = ""
        _txt += "DATE      : %s\n" % (self.date,)
        _txt += "TYPE      : %s\n" % (self.err_type,)
        _txt += "VALUE     : %s\n" % (self.err_value,)
        _txt += "VERSION   : %s\n" % (self.version,)
        _txt += "%s\n" % (self.traceback,)

        return _txt

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
def SCR_Err_Net(err_type, err_value, err_traceback):

    _err = SCR_Err(err_type, err_value, err_traceback)

    _err.save()


            

