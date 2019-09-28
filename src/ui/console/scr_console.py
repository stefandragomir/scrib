
from PyQt5.QtCore                       import *
from PyQt5.QtGui                        import *
from PyQt5.QtWidgets                    import * 
from ui.base_widgets.scr_base_widgets   import SCR_WDG_PlainTextEdit

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_Console(QWidget):


    def __init__(self):

        QWidget.__init__(self)

        self.__create_gui()

    def __create_gui(self):

        self.text = SCR_WDG_PlainTextEdit()
        self.text.setStyleSheet('background: #080008; color:#999999; ')
        self.text.setFont(QFont("Courier", 9));

        #set console to read-only
        self.text.setReadOnly(True)      
        self.text.setContextMenuPolicy(Qt.NoContextMenu)      

        self.input = QLineEdit()
        self.input.setStyleSheet('background: gray; color: white;')

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.text)
        self.setLayout(vertical_layout)

    def write(self,txt,level):

        pass



