from PyQt5 import QtWidgets, uic, QtGui, QtCore
import sys, os, json, configparser, time 
import Resources

class MainWindow(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.version="1.2.0α"
        self.ui = uic.loadUi("UI/Main.ui")
        self.ui.setWindowTitle("PY-CHR v"+self.version)
        self.parseSettings()
        self.localize()
        self.ui.show()
        self.resizeGraphics()
        self.resized.connect(self.resizeGraphics)
        self.graphicsTest()
    def resizeEvent(self, event):
        super(MainWindow, self).resizeEvent(event)
        print ("ResizeEvent triggered")
        self.resizeGraphics()
    def localize(self):
        self.locale = configparser.ConfigParser()
        self.locale.optionxform = str #making it case-insensitive
        if os.path.isfile("pychr.lang"):
            self.locale.read("pychr.lang",encoding="utf-8")
        self.localizedData = self.locale[self.config['PY-CHR']['language']]
        for key in self.localizedData:
            attr = getattr(self.ui, key)
            if str(type (attr)) == "<class 'PyQt5.QtWidgets.QMenu'>":
                attr.setTitle(self.localizedData[key])
            elif str(type (attr)) == "<class 'PyQt5.QtWidgets.QAction'>" or str(type (attr)) == "<class 'PyQt5.QtWidgets.QPushButton'>" or str(type (attr)) == "<class 'PyQt5.QtWidgets.QLabel'>":
                attr.setText(self.localizedData[key])
        setattr (self.ui, key, attr)
        #self.ui.menuHelpAbout.triggered.connect(self.buttonClickAbout)
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
        print(windows)

    def resizeGraphics(self):
        print("Resizing Graphics")

        if self.ui.pictureGL.width() < self.ui.pictureGL.height():
            self.ui.pictureGL.setFixedWidth(self.ui.pictureGL.height())
            self.ui.pictureGL.setFixedHeight(self.ui.pictureGL.width())
        elif self.ui.pictureGL.width() >  self.ui.pictureGL.height(): 
            self.ui.pictureGL.setFixedHeight(self.ui.pictureGL.width())
            self.ui.pictureGL.setFixedWidth(self.ui.pictureGL.height())
        self.ui.pictureGL.setSizePolicy(0, 0)

        if self.ui.editorGL.width() < self.ui.editorGL.height():
            self.ui.editorGL.setFixedWidth(self.ui.editorGL.height())
            self.ui.editorGL.setFixedHeight(self.ui.editorGL.width())
        elif self.ui.editorGL.width() >  self.ui.editorGL.height(): 
            self.ui.editorGL.setFixedHeight(self.ui.editorGL.width())
            self.ui.editorGL.setFixedWidth(self.ui.editorGL.height())
        self.ui.editorGL.setSizePolicy(0, 0)
    def graphicsTest(self): 
        pass

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
        print(self.index)

flag = [1]
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    windows = [MainWindow()]
    sys.exit(app.exec_())