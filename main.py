from PyQt5 import QtWidgets, uic, QtGui
import sys, os, json, configparser
import Resources

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.version="1.0.0α"
        self.ui = uic.loadUi("UI/Main.ui")
        self.ui.setWindowTitle("PY-CHR v"+self.version)
        self.parseSettings()
        self.localize()
        print(type(self.ui.GLPicture))
        self.ui.GLPicture = QSquareOpenGLWidget()
        self.ui.GLEditor = QSquareOpenGLWidget()
        print(type(self.ui.GLPicture))
        self.ui.show()
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

class QSquareOpenGLWidget(QtWidgets.QOpenGLWidget):
    def __init__(self):
        super().__init__()
    
    def heightForWidth(self, w):
        return w


    def closeEvent(self, event):
        del windows[self.index]
        event.accept()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    windows = [MainWindow()]
    sys.exit(app.exec_())