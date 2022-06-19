version = "1.5.0α:0005"

from PyQt5 import QtWidgets, uic, QtGui, QtCore
import sys, os, json, configparser, time, Resources
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi("UI/Main.ui")
        self.ui.setWindowTitle("PY-CHR v"+version)
        self.parseSettings()
        self.localize()
        self.ui.comboGUISize.activated.connect(self.resizeAction)
        self.blockSize = 8
        self.pic = 0
        #self.importPlugins()
        self.ui.centralwidget.resizeEvent = self.resizeEvent
        self.ui.graphicsPicture.mouseMoveEvent = self.mousetrack
        self.ui.show()
        self.resizeGraphics()
    def mousetrack(self,event):
        pic = self.ui.graphicsPicture
        print('pss', event.x()//((pic.width()-pic.verticalScrollBar().width())/16), event.y()//(pic.height()/16))
    def resizeEvent(self, event):
        self.resizeGraphics()
        return super(MainWindow, self).resizeEvent(event)
    def localize(self):
        comboboxFlag = 0
        combobox = 0
        self.locale = configparser.ConfigParser()
        self.locale.optionxform = str #making it case-insensitive
        if os.path.isfile("pychr.lang"):
            self.locale.read("pychr.lang",encoding="utf-8")
        self.localizedData = self.locale[self.config['PY-CHR']['language']]
        for key in self.localizedData:
            try:
                attr = getattr(self.ui, key)
            except:
                if comboboxFlag == 1:
                    combobox.setItemText(combobox.findText(key), self.localizedData[key] if ("⍼" not in self.localizedData[key]) else self.localizedData[key][:len(self.localizedData[key])-1])
                    if "⍼" in self.localizedData[key]:
                        comboboxFlag = 0
                continue
            #Checking if it's a combobox that needs translated elements
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

    def parseSettings(self):
        self.config = configparser.ConfigParser()
        if os.path.isfile("pychr.cfg"):
            self.config.read("pychr.cfg",encoding="utf-8")
        else:
            self.config['PY-CHR'] = {
                'language': 'en_us',
                'recent': (json.loads("[]")),
                'recentFormat': 0
            }
            with open("pychr.cfg", 'w') as file:
                self.config.write(file)
    #Actions for buttons
    def buttonClickAbout(self):
        windows.append(AboutWindow(self, len(windows)))
    def resizeAction(self):
        number = self.ui.comboGUISize.currentIndex()
        if number == 0:
            return
        numbers = [256,384,512,640,768,896,1024,1280,1536,1792,2048,3072,4096]
        self.ui.frame_3.setMinimumSize(numbers[number-1],numbers[number-1])
        self.ui.frame_3.setMaximumSize(numbers[number-1],numbers[number-1])
        self.resizeGraphics()
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

        if self.ui.frame_2.width() < self.ui.frame_2.height():
            diff = int((self.ui.frame_2.height() - self.ui.frame_2.width())/2)
            self.ui.frame_2.setContentsMargins(0,diff,0,diff)
        elif self.ui.frame_2.width() > self.ui.frame_2.height(): 
            diff = int((self.ui.frame_2.width() - self.ui.frame_2.height())/2)
            self.ui.frame_2.setContentsMargins(diff,0,diff,0)
        else:
            self.ui.frame_2.setContentsMargins(0,0,0,0)
        #Deez buttns
        #I'm going nuts over this
        h = int(self.ui.buttonJumpFrame.height()/12) - 5
        w = int(self.ui.buttonJumpFrame.width()/1.5)
        for i in ["Begin", "M100", "M10", "M1", "M1b", "P1b", "P1", "P10", "P100", "End","AddressInput"]:
            attr = getattr(self.ui, "buttonJump"+i)
            attr.setIconSize(QtCore.QSize(w,h))
    def graphicsTest(self):
        gp = self.ui.graphicsPicture
        ge = self.ui.graphicsEditor
        gpsize = gp.width() - gp.width()%128
        gpscale = gpsize / 128
        gpscene = QtWidgets.QGraphicsScene(0,0, gpsize, gpsize*4)

        brushes = [QtGui.QBrush(QtGui.QColor(0,0,0,255)), QtGui.QBrush(QtGui.QColor(255,0,0,255))]
        pen = QtGui.QPen(QtGui.QColor(255,0,0,0))
        for x in range (0, 128):
            for y in range (0, 128):
                gpscene.addRect(x*gpscale,y*gpscale,gpscale,gpscale,pen,brushes[(x+y)%2])
                # gpscene.addRect(x,y,1,1,pen,brushes[(x+y)%2])

        gp.setScene(gpscene)
class AboutWindow(QtWidgets.QDialog):
    def __init__(self, main, index):
        super().__init__()
        self.version = main.version
        self.ui = uic.loadUi("Ui/About.ui")
        self.ui.setWindowTitle("PY-CHR v"+self.version+" - About")
        self.ui.dialogAboutVersion.setText("PY-CHR v"+self.version)
        self.ui.closeEvent = self.closeEvent
        self.ui.show()
        self.index = index

flag = [1]
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    windows = [MainWindow()]
    sys.exit(app.exec_())