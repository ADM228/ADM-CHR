#About to get deleted
from ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
#because
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import sys, json, configparser, os, Resources

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Loading...")

        #self.gpsize = self.ui.graphicsPicture.width() - self.ui.graphicsPicture.width()%128
        #self.gpscale = self.gpsize / 128
        #self.gpscene = QtWidgets.QGraphicsScene(0,0, self.gpsize, self.gpsize*4)
        #self.ui.graphicsPicture.setScene(self.gpscene)
        #self.resizeGraphics() 

        self.version="2.0.0α"
        self.set_title("PY-CHR v" + self.version)
        #self.parseSettings()
        #self.localize()
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        #print(self.ui.graphicsPicture.width(), self.ui.graphicsPicture.height(), self.ui.graphicsPicture.sizePolicy().horizontalPolicy(),  self.ui.graphicsPicture.sizePolicy().verticalPolicy())
        #print(self.ui.graphicsEditor.width(), self.ui.graphicsEditor.height(), self.ui.graphicsEditor.sizePolicy().horizontalPolicy(),  self.ui.graphicsEditor.sizePolicy().verticalPolicy())
        #self.graphicsTest()
    # def resizeEvent(self, event):
    #     print ("ResizeEvent triggered")
    #     self.resizeGraphics()
    #     return super(MainWindow, self).resizeEvent(event)
    def resizeGraphics(self):
        print("Resizing Graphics")
        # print(self.ui.graphicsPicture.width(), self.ui.graphicsPicture.height(), self.ui.graphicsPicture.sizePolicy().horizontalPolicy(),  self.ui.graphicsPicture.sizePolicy().verticalPolicy())
        # if self.ui.graphicsPicture.width() >= self.ui.graphicsPicture.height():
        #     self.ui.graphicsPicture.setFixedHeight(self.ui.graphicsPicture.width())
        #     self.ui.graphicsPicture.setFixedWidth(self.ui.graphicsPicture.height())
        #     self.ui.graphicsPicture.setSizePolicy(0, 0)
        # else: 
        #     self.ui.graphicsPicture.setFixedWidth(self.ui.graphicsPicture.height())
        #     self.ui.graphicsPicture.setFixedHeight(self.ui.graphicsPicture.width())
        #     self.ui.graphicsPicture.setSizePolicy(0, 0)
        # print(self.ui.graphicsPicture.width(), self.ui.graphicsPicture.height(), self.ui.graphicsPicture.sizePolicy().horizontalPolicy(),  self.ui.graphicsPicture.sizePolicy().verticalPolicy())

        # print(self.ui.graphicsEditor.width(), self.ui.graphicsEditor.height(), self.ui.graphicsEditor.sizePolicy().horizontalPolicy(),  self.ui.graphicsEditor.sizePolicy().verticalPolicy())
        # if self.ui.graphicsEditor.width() >= self.ui.graphicsEditor.height():
        #     self.ui.graphicsEditor.setFixedHeight(self.ui.graphicsEditor.width())
        #     self.ui.graphicsEditor.setFixedWidth(self.ui.graphicsEditor.height())
        #     self.ui.graphicsEditor.setSizePolicy(0, 0)
        # else: 
        #     self.ui.graphicsEditor.setFixedWidth(self.ui.graphicsEditor.height())
        #     self.ui.graphicsEditor.setFixedHeight(self.ui.graphicsEditor.width())
        #     self.ui.graphicsEditor.setSizePolicy(0, 0)
        # print(self.ui.graphicsEditor.width(), self.ui.graphicsEditor.height(), self.ui.graphicsEditor.sizePolicy().horizontalPolicy(),  self.ui.graphicsEditor.sizePolicy().verticalPolicy())
    def localize(self):
        self.locale = configparser.ConfigParser()
        self.locale.optionxform = str #making it case-insensitive
        if os.path.isfile("pychr.lang"):
            self.locale.read("pychr.lang",encoding="utf-8")
        self.localizedData = self.locale[self.config['PY-CHR']['language']]
        # for key in self.localizedData:
        #     attr = getattr(self.ui, key)
        #     if str(type (attr)) == "<class 'PyQt5.QtWidgets.QMenu'>":
        #         attr.setTitle(self.localizedData[key])
        #     elif str(type (attr)) == "<class 'PyQt5.QtWidgets.QAction'>" or str(type (attr)) == "<class 'PyQt5.QtWidgets.QPushButton'>" or str(type (attr)) == "<class 'PyQt5.QtWidgets.QLabel'>":
        #         attr.setText(self.localizedData[key])
        # setattr (self.ui, key, attr)
        # #self.ui.menuHelpAbout.triggered.connect(self.buttonClickAbout)
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
    def graphicsTest(self):
        pass

windows = [MainWindow()]
main = windows[0]
Gtk.main()