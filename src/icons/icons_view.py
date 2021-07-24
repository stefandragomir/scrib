
import base64
import pyperclip
import os
import sys
import itertools
import shutil

from PIL              import Image
from hashlib          import sha1
from functools        import partial
from datetime         import datetime
from PyQt5.QtCore     import * 
from PyQt5.QtGui      import * 
from PyQt5.QtWidgets  import * 

try:
    _path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
    _path = os.path.split(_path)[0]
    sys.path.append(_path)
except:
    pass 

from icons          import SCR_GetIcon
from icons          import SCR_GetPixmap
from icons          import SCR_GetByteArray
from icons          import SCR_GetIconNames
from icons          import SCR_As_Icon
from icons          import SCR_As_Pixmap
from icons          import SCR_Database
from icons_view_css import CSS

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_IconsMainApp(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        self.centralWidget = SCR_IconsViewer(self)

        self.setCentralWidget(self.centralWidget)

        self.setWindowTitle("SCR Icons")
        
        self.setWindowIcon(SCR_GetIcon("fd2cf51bcbd304d61dbae1fdd954d4d1ec41e535", "large"))

        self.setFixedSize(1150, 790)  

        self.createToolbar()

        self.setStyleSheet(CSS)

    def createToolbar(self):

        self.toolBar = self.addToolBar('Main Toolbar')

        self.toolBar.setMovable(False)
        
        self.addImageAction  =  QAction(SCR_GetIcon("b73feb17d8389b0eab7a8a0de2d0b3c7a2f8f62c"),'Add Image',self)
        
        self.addImageAction.triggered.connect(self.addImageClicked)
        
        self.toolBar.addAction(self.addImageAction)

    def addImageClicked(self):

        filesSelected = QFileDialog.getOpenFileNames(self,"Select one or more images:","","File Format( *.png ")
        imagesOk = []
        imagesNOk = []
        for image in filesSelected[0]:
            im = Image.open(image)
            width, height = im.size
            if width != height or width < 50:
                imagesNOk.append(image)
                
            else:
                imagesOk.append(image)
        

        if len(imagesNOk):
            if len(imagesNOk)>1:
                errorText = 'Images : ' + ','.join(imagesNOk) +' are not in the expected format! Image height and width should be equal and image dimension should be at least 50x50 pixels!'
            else:
                errorText = 'Image : ' + str(imagesNOk[0]) +' is not in the expected format! Image height and width should be equal and image dimension should be at least 50x50 pixels!'
            self.internalPopUp = SCR_Info(self,"Error",errorText,QMessageBox.Critical)

        if len(imagesOk):
            self.iconInserterWindow = SCR_IconInserter(self.centralWidget.databaseConnection,imagesOk)
            if self.iconInserterWindow.accepted:
                self.centralWidget._Tree_Icons._add_to_watch()
            QApplication.restoreOverrideCursor()
        
"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_IconInserter(QDialog):

    def __init__(self,dbConnection,imagesPath):

        QDialog.__init__(self)

        self.setWindowTitle("Add Icon")
        
        self.setWindowIcon(SCR_GetIcon("fd2cf51bcbd304d61dbae1fdd954d4d1ec41e535", "large"))

        self.dbConnection = dbConnection
        self.imagesPath = imagesPath
        self.myDict = {}
        self.buildUI()
        self.setStyleSheet(CSS)
        self.setModal(True)
        self.accepted = False
        self.exec()

    def buildUI(self):

        self.layout = QGridLayout()
        position = 0
        self.myDict = {}
        for image in self.imagesPath:
            img = Image.open(image)
            img.thumbnail((50,50), Image.ANTIALIAS)
            img.save(r"resized.png", "PNG")
            imageLabel = QLabel("Image")
            newImage = QLabel()
            newImage.setPixmap(QPixmap.fromImage(QImage(r"resized.png")))
            tagLabel = QLabel("Tags")
            newTags = QPlainTextEdit()
            newTags.setFixedHeight(50)
            newTags.setPlaceholderText("Insert tags for the image in the following format: tag1,tag2,tag3...")

            self.layout.addWidget(imageLabel,position,0)
            self.layout.addWidget(newImage,position+1,0)
            self.layout.addWidget(tagLabel,position,1)
            self.layout.addWidget(newTags,position+1,1)

            position = position + 3

            self.myDict[image] = newTags

            os.remove(r"resized.png")

        self.buttons = QDialogButtonBox()
        self.buttons.setStandardButtons(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.layout.addWidget(self.buttons ,position,1)

        self.buttons.accepted.connect(partial(self.saveImages,True))
        self.buttons.rejected.connect(partial(self.saveImages,False))

        self.setLayout(self.layout)

    def saveImages(self,save):
        if save:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            for key in self.myDict.keys():
                base64Dict = {}
                timestampStr = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
                hashableData = (self.myDict[key].toPlainText() + timestampStr).encode()
                sha1Result   = sha1(hashableData).hexdigest()
                _temp_path = os.path.abspath("temp")
                if not os.path.exists(_temp_path):
                    os.mkdir(_temp_path)
                newPath = os.path.join(_temp_path,sha1Result)
                os.mkdir(newPath)
                #create the 3 images in format 15*15, 30*30 nad 50*50 and save them in the new created directory
                for size in ((15,15),(30,30),(50,50)):
                    img = Image.open(key)
                    img.thumbnail(size, Image.ANTIALIAS)
                    newFilePath = newPath + "\\" + str(size[0])+"_"+str(size[1])+".png"
                    img.save(newFilePath, "PNG")
                    base64Dict[str(size[0])+"_"+str(size[1])] = base64.b64encode(open(newFilePath, "rb").read()).decode('ascii')
                #save the images in the database file
                newElementDb = {}
                newElementDb['name']       = str(sha1Result) 
                tags = self.myDict[key].toPlainText()
                newElementDb['tags']       = tags
                newElementDb['img_small']  = base64Dict["15_15"]
                newElementDb['img_medium'] = base64Dict["30_30"]
                newElementDb['img_large']  = base64Dict["50_50"] 

                self.dbConnection.insert(newElementDb)

                shutil.rmtree(newPath)
                shutil.rmtree(_temp_path)

            self.accepted = True

        self.accept()

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_IconsViewer(QWidget): 

    def __init__(self,parent):

        QWidget.__init__(self)

        self.parent = parent

        dbPath = os.path.join(os.path.split(os.path.abspath(__file__))[0],"icons.db")

        self.databaseConnection = SCR_Database(dbPath)

        self._create_gui()

        self.setAcceptDrops(True)

        self.droppedFiles = []

    def _create_gui(self):

        self.setWindowTitle("Icon Viewer")
        self.setMinimumWidth(750)
        self._Tree_Icons      = SCR_Tree_Icons(self)
        self._Icons_Attribute = SCR_IconsAtributes(self)
        self.TreeAreaWidget = QWidget() 

        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self._tags_label  = QLabel('Tags:')         
        self._tags_label.setFont(font)

        self._tags = QLineEdit()
        self.toolbar_layout = QGridLayout()
        self.toolbar_layout.addWidget(self._tags_label, 0,0)
        self.toolbar_layout.addWidget(self._tags)
        self.toolbar_layout.setAlignment(Qt.AlignLeft )

        self.tree_area = QVBoxLayout() 
        self.tree_area.addLayout(self.toolbar_layout) 
        self.tree_area.addWidget(self._Tree_Icons) 
        self.TreeAreaWidget.setLayout(self.tree_area)

        _splitter = QSplitter(Qt.Horizontal)
        _splitter.addWidget(self.TreeAreaWidget)
        _splitter.addWidget(self._Icons_Attribute)
        
        _layout = QHBoxLayout()
        _layout.addWidget(_splitter)        
        _layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(_layout)

        self._tags.textChanged.connect(self._handle_tags)

    def _handle_tags(self):

        icons = self.databaseConnection.get_all_table_rows()
        searchText = self._tags.text() 
        tagsMatch = [icon[1] for icon in icons if searchText in icon[2]]
        nameMatch = [icon[1] for icon in icons if searchText in icon[1]]
        
        self._Tree_Icons._update_tree(tagsMatch + nameMatch)

    def dragEnterEvent(self,event):

        acceptEvent = False
        urlsDragged =  event.mimeData().urls()

        for url in urlsDragged:

            if url.toLocalFile().lower().endswith(('.png')):
                acceptEvent = True
            else:
                acceptEvent = False
                break

        if acceptEvent:
            self.droppedFiles = [url.toLocalFile() for url in urlsDragged]
            event.acceptProposedAction()
        
    def dropEvent(self,event):

        imagesOk = []
        imagesNOk = []
        for image in self.droppedFiles:
            im = Image.open(image)
            width, height = im.size
            if width != height or width < 50:
                imagesNOk.append(image)
                
            else:
                imagesOk.append(image)
        

        if len(imagesNOk):
            if len(imagesNOk)>1:
                errorText = 'Images : ' + ','.join(imagesNOk) +' are not in the expected format! Image height and width should be equal and image dimension should be at least 50x50 pixels!'
            else:
                errorText = 'Image : ' + str(imagesNOk[0]) +' is not in the expected format! Image height and width should be equal and image dimension should be at least 50x50 pixels!'
            self.internalPopUp = SCR_Info(self,"Error",errorText,QMessageBox.Critical)

        if len(imagesOk):
            self.iconInserterWindow = SCR_IconInserter(self.databaseConnection,imagesOk)
            if self.iconInserterWindow.accepted:
                self._Tree_Icons._add_to_watch()
            QApplication.restoreOverrideCursor()

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_IconsAtributes(QWidget):

    items = []

    def __init__(self, parent):

        QWidget.__init__(self)
        self._parent = parent
        self._create_gui()

    def _create_gui(self):

        # name label
        self._bus_name   = QLabel()
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.setMaximumWidth(750)

        _spacer = QWidget()             
        _spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)

        # Labels
        self._small_icon_label  = QLabel('Small (15x15)')       
        self._small_icon_label.setFont(font)
        self._small_icon_label.setAlignment(Qt.AlignCenter)

        self._medium_icon_label  = QLabel('Medium (30x30)')         
        self._medium_icon_label.setFont(font)
        self._medium_icon_label.setAlignment(Qt.AlignCenter)

        self._large_icon_label  = QLabel('Large (50x50)')           
        self._large_icon_label.setFont(font)
        self._large_icon_label.setAlignment(Qt.AlignCenter)

        self._small_icon = QLabel()
        self._small_icon.setPixmap(SCR_As_Pixmap(self._parent.databaseConnection.get_row_by_name('fd2cf51bcbd304d61dbae1fdd954d4d1ec41e535')[3]))
        self._small_icon.setAlignment(Qt.AlignCenter)


        self._medium_icon = QLabel()
        self._medium_icon.setPixmap(SCR_As_Pixmap(self._parent.databaseConnection.get_row_by_name('fd2cf51bcbd304d61dbae1fdd954d4d1ec41e535')[4]))
        self._medium_icon.setAlignment(Qt.AlignCenter)

        self._large_icon = QLabel()
        self._large_icon.setPixmap(SCR_As_Pixmap(self._parent.databaseConnection.get_row_by_name('fd2cf51bcbd304d61dbae1fdd954d4d1ec41e535')[5]))
        self._large_icon.setAlignment(Qt.AlignCenter)


        self.IconCode_label  = QLabel("Code")           
        self.IconCode_label.setFont(font)

        self._font = QFont()
        self._font.setPointSize(8)
        self._font.setBold(True)

        self.IconCode = QPlainTextEdit()
        self.IconCode.setAcceptDrops(False)
        self.IconCode.setFont(self._font)
        self.IconCode.setContextMenuPolicy(Qt.NoContextMenu)
        self.IconCode.setMinimumSize(650, 450)

        self.IconCode_layout = QGridLayout()
        self.IconCode_layout.addWidget(self.IconCode_label, 0,0)
        self.IconCode_layout.addWidget(self.IconCode)
        self.IconCode_layout.setAlignment(Qt.AlignLeft )

        _preview_group_box = QGroupBox("Icons")
        _preview_group_box.setFont(font)
        _preview_group_box.setAlignment(Qt.AlignLeft)
        _preview_group_box.setMinimumSize(650, 150)     

        _preview_Icons_layout = QGridLayout()   
        _preview_Icons_layout.addWidget(self._small_icon_label,0,0)
        _preview_Icons_layout.addWidget(self._small_icon,1,0)
        _preview_Icons_layout.addWidget(self._medium_icon_label,0,1)
        _preview_Icons_layout.addWidget(self._medium_icon,1,1)
        _preview_Icons_layout.addWidget(self._large_icon_label,0,2)
        _preview_Icons_layout.addWidget(self._large_icon,1,2)

        _preview_group_box.setLayout(_preview_Icons_layout)

        self.lbl_tag = QLineEdit()
        self.lbl_tag.setReadOnly(True)

        _ly_tag = QHBoxLayout()
        _ly_tag.addWidget(self.lbl_tag)

        _tag_group_box = QGroupBox("Name")
        _tag_group_box.setFont(font)
        _tag_group_box.setAlignment(Qt.AlignLeft)
        _tag_group_box.setMinimumSize(650, 70)  
        _tag_group_box.setLayout(_ly_tag)

        _main_layout = QVBoxLayout()
        _main_layout.addWidget(_tag_group_box)
        _main_layout.addWidget(_preview_group_box)
        _main_layout.addLayout(self.IconCode_layout)
        _main_layout.addWidget(_spacer) 
        self.setLayout(_main_layout)

    def _icon_changed(self, icon_name):

        self._small_icon.setPixmap(SCR_GetPixmap(icon_name, 'small'))
        self._medium_icon.setPixmap(SCR_GetPixmap(icon_name, 'medium'))
        self._large_icon.setPixmap(SCR_GetPixmap(icon_name, 'large'))
        self.lbl_tag.setText(icon_name)
        self._update_IconCode(icon_name)

    def _update_IconCode(self,icon_name):

        _txt = """
        from  icons import SCR_GetIcon
        from  icons import SCR_GetPixmax
        from  icons import SCR_GetByteArray

        SCR_GetIcon("%s", "small")

        SCR_GetIcon("%s", "medium")

        SCR_GetIcon("%s", "large")



        SCR_GetPixmax("%s", "small")

        SCR_GetPixmax("%s", "medium")

        SCR_GetPixmax("%s", "large")



        SCR_GetByteArray("%s", "small")

        SCR_GetByteArray("%s", "medium")

        SCR_GetByteArray("%s", "large")

        """ % (icon_name,icon_name,icon_name,icon_name,icon_name,icon_name,icon_name,icon_name,icon_name)

        self.IconCode.clear()

        self.IconCode.insertPlainText(_txt)

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_Tree_Icons(QTreeWidget):

    _headers = ['Icons']

    def __init__(self, parent):

        QTreeWidget.__init__(self)
        self._parent = parent

        self.create_gui()

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.treeContextMenu)

    def create_gui(self):

        _header_font = QFont("" , 10 , QFont.Bold )      
        self.setHeaderLabels(self._headers)              
        self.setSortingEnabled(True)

        self.setColumnCount(len(self._headers))                         
        self.setSelectionBehavior(QAbstractItemView.SelectRows)    
        self.setAnimated(True)  

        self.itemClicked.connect(self._display_icon_selected)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.__resize_cols()
        self._add_to_watch()

    def _display_icon_selected(self, item, col):

        self._parent._Icons_Attribute._icon_changed(item.text(0))

    def __resize_cols(self):

        for _col_idx in range(self.columnCount()):
            self.resizeColumnToContents(_col_idx) 

    def _add_to_watch(self):

        self.clear()
        sw_iconsNames = self._parent.databaseConnection.get_names()

        for _icon_name in sw_iconsNames:

            item = QTreeWidgetItem()
            item.setChildIndicatorPolicy(QTreeWidgetItem.DontShowIndicatorWhenChildless)   
            self.addTopLevelItem(item)

            _column = 0 
            item.setIcon(_column, SCR_As_Icon(self._parent.databaseConnection.get_row_by_name(_icon_name)[3]))  
            item.setData(_column, Qt.EditRole, _icon_name)
            self.invisibleRootItem().addChild(item)                       
            self.__resize_cols() 

    def _update_tree(self, items):

        treeItems     = [self.topLevelItem(treeItemNo) for treeItemNo in range(self.topLevelItemCount())]
        treeItemsText = [treeItem.text(0) for treeItem in treeItems]
        
        for treeItemText in treeItemsText:
            if treeItemText in items:
                treeItems[treeItemsText.index(treeItemText)].setHidden(False)
            else: 
                treeItems[treeItemsText.index(treeItemText)].setHidden(True)

    def treeContextMenu(self,coordinates):

        item = self.itemAt(coordinates)
        if item:
            SCR_TreeContextMenu(self,item,['Get Name','Get Tags','Get 15x15 Base64','Get 30x30 Base64','Get 50x50 Base64','Delete from Database','Save 15x15',"Save 30x30","Save 50x50"])

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_TreeContextMenu(QMenu):

    def __init__(self,parent,treeItem,menuOptions):

        QMenu.__init__(self)
        self.menuOptions = menuOptions
        self.parent      = parent
        self.treeItem    = treeItem
        self.createOptions()

        self.triggered.connect(self.menuActionTriggered)

        self.setStyleSheet(CSS)
        self.runMenu()

    def runMenu(self):

        self.exec(QCursor.pos())

    def createOptions(self):

        for menuOption in self.menuOptions:

            self.addAction(menuOption)

    def save_image(self,name,size,pixmap):

        _path = "%s_%s.png" % (name,size)

        _file = QFile(_path)

        _file.open(QIODevice.WriteOnly)

        pixmap.save(_file, "PNG");

        os.startfile(_path)
            
    def menuActionTriggered(self,menuAction):

        itemText = self.treeItem.text(0)
        record = self.parent._parent.databaseConnection.get_row_by_name(itemText)
        if record:
            if menuAction.text() == "Get Name":
                pyperclip.copy(record[1])
            elif menuAction.text() == 'Get Tags':
                pyperclip.copy(record[2])
            elif menuAction.text() == 'Get 15x15 Base64':
                pyperclip.copy(record[3])
            elif menuAction.text() == 'Get 30x30 Base64':
                pyperclip.copy(record[4])
            elif menuAction.text() == 'Get 50x50 Base64':
                pyperclip.copy(record[5])
            elif menuAction.text() == 'Delete from Database':
                QApplication.setOverrideCursor(Qt.WaitCursor)

                self.parent._parent.databaseConnection.get_row_by_name(itemText)
                #repopuplate tree with data form db
                self.parent._add_to_watch()
                #apply selected filter form tags input
                self.parent._parent._tags.textChanged.emit(self.parent._parent._tags.text())

                QApplication.restoreOverrideCursor()

            elif menuAction.text() == 'Save 15x15':

                self.save_image(itemText,"small",SCR_GetPixmap(itemText,"small"))

            elif menuAction.text() == 'Save 30x30':

                self.save_image(itemText,"medium",SCR_GetPixmap(itemText,"medium"))

            elif menuAction.text() == 'Save 50x50':

                self.save_image(itemText,"large",SCR_GetPixmap(itemText,"large"))

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_Info(QMessageBox):

    def __init__(self,parent,title,text,boxType = QMessageBox.Critical):

        self.boxType   = boxType
        QInputDialog.__init__(self,self.boxType,title,text,QMessageBox.Ok)
        self.parent = parent
        self.setStyleSheet(CSS)
        self.setModal(True)
        self.exec()

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
if __name__ == "__main__":

    _app    = QApplication(sys.argv)

    _window = SCR_IconsMainApp()

    _window.show()

    sys.exit(_app.exec_())  
