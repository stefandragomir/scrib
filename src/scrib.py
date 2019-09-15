
import os
import sys

try:
    _path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
    sys.path.append(_path)
except:
    pass

_path = os.path.split(os.path.split(os.path.abspath("__file__"))[0])[0]
sys.path.append(_path)

from PyQt5.QtCore                                                      import *
from PyQt5.QtGui                                                       import *
from PyQt5.QtWidgets                                                   import * 

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_UI(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        self.draw_gui() 

    def draw_gui(self):
        #Define Ghost Manager interface aspect

        self.setWindowTitle("Robot Framework Scrib")
        self.setMinimumSize(1300, 800)       
        self.setMinimumHeight(500)

        self.wdg_central = QWidget()

        self.setCentralWidget(self.wdg_central)
        self.activateWindow()

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
if __name__ == "__main__":

    _app = QApplication(sys.argv)  
    _ui  = SCR_UI()           
    _ui.show()
    sys.exit(_app.exec_())


