#   CODE UPDATES BY CONNORWILLCHRIS
#
# --11/3/2023
#
# The changes I made are mostly organizational changes. Some of them required,
# some of them for myself, but the code *should* be easier to read now

# changed the Alpha symbol to a (why use the alpha symbol for alpha anyways? lol)
version = "1.5.0a:0007"

from PyQt5 import QtWidgets, uic, QtGui, QtCore
import sys, os, json, configparser, time

# OUR IMPORTS (forgive me, this is easier for me to understand)
import Resources, QGoodButton

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # init
        super(MainWindow, self).__init__()

        # class variables reorganized (mostly to be easier to read)
        self.ui = uic.loadUi("UI/Main.ui")
        self.blockSize = 8
        self.pic = 0

        self.ui.setWindowTitle("PY-CHR v"+version)
        self.ui.comboGUISize.activated.connect(self.resizeAction)
        
        self.addButtons()
        self.parseSettings()
        self.localize()

        self.buttonPaletteTable()
        self.ui.buttonPaletteTable.clickedConnect(self.buttonPaletteTable)

        #self.importPlugins()
        self.ui.centralwidget.resizeEvent = self.resizeEvent
        self.ui.graphicsPicture.mouseMoveEvent = self.mousetrack
        self.ui.show()

        self.resizeGraphics()

    def addButtons(self):
        #first the jump buttons
        jumpButtonList = ["Begin", "M100", "M10", "M1", "M1b", "P1b", "P1", "P10", "P100", "End"]
        jumpButtonImageList = ["BeginningOfFile", "Block-100", "Block-10", "Block-1", "Byte-1", "Byte+1", "Block+1", "Block+10", "Block+100", "EndOfFile"]

        # I declared this variable as the QGoodButton type, to make it easier to understand
        attr: QGoodButton

        for button in range(len(jumpButtonList)):

            # I made this easier to read in general, by using string.format
            attr = QGoodButton.QGoodButton(":/buttonJump/{}.png".format(jumpButtonImageList[button]))

            setattr(self.ui, "buttonJump" + jumpButtonList[button], attr)

            # you can make stringing functions like this, to make it easier to read!
            self.ui.buttonJumpFrame.layout()\
                .addWidget(attr)

        #then the regular buttons

        # updated it to look nicer ;)
        buttonList =\
        [
            {
                "name": "PictureGrid",
                "filename": "PictureGrid",
                "parent": "horizontalLayout_3",
                "checkable": True
            },
            {
                "name": "EditorGrid",
                "filename": "EditorGrid",
                "parent": "horizontalLayout_3",
                "checkable": True}
        ]

        for button in buttonList:
            attr = QGoodButton.QGoodButton(":/button/{}.png".format(button["filename"]))

            # you use strings kind of inconsistantly. I suggest using one style and sticking to it!
            attr.checkable = button["checkable"]

            setattr(self.ui, "button" + button["name"], attr)
            attr2 = getattr(self.ui, button["parent"])

            if str(type(attr2)) == "<class 'PyQt5.QtWidgets.QFrame'>":
                attr2.layout().addWidget(attr)
            else:
                attr2.addWidget(attr)

        # then the one mode switch
        self.ui.buttonPaletteTable = QGoodButton.QModeSwitch([":/button/Palette.png", ":/button/PaletteTable.png"])

        self.ui.framePalette.layout()\
            .addWidget(self.ui.buttonPaletteTable)

    # records the mouse's position in the box-window for editing CHRs
    def mousetrack(self,event):
        pic = self.ui.graphicsPicture

        # this is very unreadable. I will try to fix it         11/3/2023
        print('pss', event.x()//((pic.width()-pic.verticalScrollBar().width())/16), event.y()//(pic.height()/16))

    # this resizes the window, I presume? lol
    def resizeEvent(self, event):
        self.resizeGraphics()
        return super(MainWindow, self)\
            .resizeEvent(event)
    
    # 11/1/2023     DONE
    #
    # I think *nihonga* is japanese for "the language Japanese" btw
    def localize(self):
        comboboxFlag = 0
        combobox = 0

        self.locale = configparser.ConfigParser()
        self.locale.optionxform = str #making it case-insensitive

        if os.path.isfile("pychr.lang"):
            self.locale.read("pychr.lang", encoding="utf-8")
        self.localizedData = self.locale[self.config['PY-CHR']['language']]

        for key in self.localizedData:

            try:
                attr = getattr(self.ui, key)

            except:
                if comboboxFlag == 1:
                    # why "⍼" and not something more *orthodox* ?
                    combobox.setItemText(combobox.findText(key), self.localizedData[key] if ("⍼" not in self.localizedData[key]) else self.localizedData[key][:len(self.localizedData[key])-1])

                    # why "⍼" and not something more *orthodox* ?
                    if "⍼" in self.localizedData[key]: 
                        comboboxFlag = 0
                continue

            #-Checking if it's a combobox that needs translated elements
            if str(type (attr)) == "<class 'PyQt5.QtWidgets.QComboBox'>" and self.localizedData[key] == "⍼":
                comboboxFlag = 1
                combobox = attr

                continue

            #Checking directly
            if str(type (attr)) == "<class 'PyQt5.QtWidgets.QMenu'>":
                attr.setTitle(self.localizedData[key])

            elif str(type (attr)) == "<class 'PyQt5.QtWidgets.QAction'>" or str(type (attr)) == "<class 'PyQt5.QtWidgets.QPushButton'>" or str(type (attr)) == "<class 'PyQt5.QtWidgets.QLabel'>":
                attr.setText(self.localizedData[key])

        #Localizing the tooltips
        self.localizedData = self.locale[self.config['PY-CHR']['language']+"_tooltips"]

        for key in self.localizedData:
            attr = getattr(self.ui, key)
            attr.setToolTip(self.localizedData[key])



    #Future code for the beta phase
    #==============================================================================================================
    # def importPlugins(self):
    #     if not os.path.isdir("Plugins"):
    #         QtWidgets.QMessageBox.warning(self, "PY-CHR v"+version+" Warning", "It seems that you have deleted the Plugins folder.\nIt is crucial for PY-CHR to interpret graphics. \n\n\nPlease put it back, or download PY-CHR again.")
    #         return
    #     if not os.path.isfile("Plugins/builtin.py"):
    #         QtWidgets.QMessageBox.warning(self, "PY-CHR v"+version+" Warning", "It seems that you have deleted the Plugins/builtin.py file.\nIt is crucial for PY-CHR to interpret graphics. \n\n\nPlease put it back, or download PY-CHR again.")
    #         return
    #     sys.path.insert(0, "Plugins")
    #     import builtin
    #     print(builtin.formats)
    #     builtin.interpret("1", b"040033")        
    #==============================================================================================================

    # neat system! ;)       
    def parseSettings(self):
        self.config = configparser.ConfigParser()

        if os.path.isfile("pychr.cfg"):
            self.config.read("pychr.cfg",encoding="utf-8")

        else:
            self.config['PY-CHR'] = {
                "language": "en_us",
                "recent": (json.loads("[]")),
                "recentFormat": 0
            }
            with open("pychr.cfg", "w") as file:
                self.config.write(file)


    # Actions for buttons
    # todo          work on this about section
    def buttonClickAbout(self):
        windows.append(AboutWindow(self, len(windows)))

    def resizeAction(self):
        number = self.ui.comboGUISize.currentIndex()
        if number == 0:
            return
        
        # put this into a JSON maybe?
        numbers = [256, 384, 512, 640, 768, 896, 1024, 1280, 1536, 1792, 2048, 3072, 4096]

        self.ui.frame_3.setMinimumSize(numbers[number - 1], numbers[number - 1])
        self.ui.frame_3.setMaximumSize(numbers[number - 1], numbers[number - 1])
        self.resizeGraphics()

    # todo      clean this up, it's really messy
    def resizeGraphics(self):
        if self.ui.frame_3.width() < self.ui.frame_3.height():
            diff = int((self.ui.frame_3.height() - self.ui.frame_3.width()+self.ui.graphicsPicture.verticalScrollBar().width())/2)
            self.ui.frame_3.setContentsMargins(0,diff,0,diff)

        elif self.ui.frame_3.width() > self.ui.frame_3.height() + self.ui.graphicsPicture.verticalScrollBar().width(): 
            diff = int((self.ui.frame_3.width() - self.ui.frame_3.height()-self.ui.graphicsPicture.verticalScrollBar().width())/2)
            self.ui.frame_3.setContentsMargins(diff,0,diff,0)

        else:
            diff = int((self.ui.graphicsPicture.verticalScrollBar().width() - self.ui.frame_3.width() + self.ui.frame_3.height())/2)
            self.ui.frame_3.setContentsMargins(0,diff,0,diff)
        

        self.ui.buttonJumpFrame.setMinimumSize(self.ui.graphicsPicture.width()//16,0)


        if self.ui.frame_2.width() < self.ui.frame_2.height():
            diff = int((self.ui.frame_2.height() - self.ui.frame_2.width()))
            self.ui.frame_2.setContentsMargins(0,0,0,diff)

        elif self.ui.frame_2.width() > self.ui.frame_2.height():
            diff = int((self.ui.frame_2.width() - self.ui.frame_2.height())/2)
            self.ui.frame_2.setContentsMargins(diff,0,diff,0)

        else:
            self.ui.frame_2.setContentsMargins(0,0,0,0)
        #Deez buttns
        #I'm going nuts over this
        # ... I know, right? lol


        # this variable is unused. Why?
        size = min(int(self.ui.buttonJumpFrame.width()/1.5), int(self.ui.buttonJumpFrame.height()/12) - 5)

    def buttonPaletteTable(self):
        mode = self.ui.buttonPaletteTable.mode
        if mode == 1:
            self.ui.graphicsPaletteTable.show()
        else:
            self.ui.graphicsPaletteTable.hide()

    def graphicsTest(self):
        gp = self.ui.graphicsPicture

        # This is unused. Why?
        ge = self.ui.graphicsEditor

        gpsize = gp.width() - gp.width() % 128
        gpscale = gpsize / 128
        gpscene = QtWidgets.QGraphicsScene(0, 0, gpsize, gpsize*4)

        brushes = [
            QtGui.QBrush(QtGui.QColor(0,0,0,255)), QtGui.QBrush(QtGui.QColor(255,0,0,255))
        ]

        pen = QtGui.QPen(QtGui.QColor(255,0,0,0))

        for x in range (0, 128):
            for y in range (0, 128):
                gpscene.addRect(x*gpscale,y*gpscale,gpscale,gpscale,pen,brushes[(x+y)%2])
                # gpscene.addRect(x,y,1,1,pen,brushes[(x+y)%2])

        gp.setScene(gpscene)

# Currently does nothing, according to my knowledge...
class AboutWindow(QtWidgets.QDialog):

    def __init__(self, main, index):
        super().__init__()

        self.version = main.version

        # need to create this UI/About.ui file!!
        self.ui = uic.loadUi("Ui/About.ui")
        self.index = index

        self.ui.setWindowTitle("PY-CHR v" + self.version + " - About")
        self.ui.dialogAboutVersion.setText("PY-CHR v" + self.version)
        self.ui.closeEvent = self.closeEvent
        self.ui.show()

# what is this flag supposed to do?
flag = [1]

if __name__ == "__main__":

    # are you planning on using console arguments in this app?
    app = QtWidgets.QApplication(sys.argv)

    # I know this is meant to be used as a system for multiple windows, but is
    # this really the most elegant way of doing so?
    windows = [ MainWindow() ]
    sys.exit(app.exec_())
