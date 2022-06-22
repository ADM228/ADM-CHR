from PyQt5 import QtWidgets, QtGui, QtCore
import os
class QGoodButton(QtWidgets.QFrame):
    def __init__(self, pixmap):
        super(QGoodButton, self).__init__()
        if str(type(pixmap)) == "<class 'str'>":
            self.pixmap = QtGui.QPixmap.fromImage(QtGui.QImage(pixmap))
        elif str(type(pixmap)) == "<class 'PyQt5.QtGui.QImage'>":
            self.pixmap = QtGui.QPixmap.fromImage(pixmap)
        elif str(type(pixmap)) == "<class 'PyQt5.QtGui.QPixmap'>":
            self.pixmap = pixmap
        else:
            raise TypeError("QGoodButton(self, pixmap): The 'pixmap' parameter supplied to 'QGoodButton()' isn't a string, QImage, or a QPixmap - what the fuck are you importing?")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.layout)
        self.label = QtWidgets.QLabel()
        self.layout.addWidget(self.label)
        self.layout.setContentsMargins(0,0,0,0)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Ignored,QtWidgets.QSizePolicy.Ignored)
        self.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.label.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.label.setPixmap(self.pixmap)
        self.label.setScaledContents(True)
        self.setMinimumSize(8,8)
        self.maintainAspectRatio = True
        self.checkable = False
        self.checked = False
    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken) 
        return super().mousePressEvent(ev)
    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        if not self.checkable:
            self.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        else:
            if self.checked == False:
                self.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
                self.checked = True
            else:
                self.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
                self.checked = False    
        return super().mousePressEvent(ev)
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        if self.maintainAspectRatio:
            #Setting up the margins to maintain the aspect ratio
            if self.width() < self.height():
                diff = int((self.height() - self.width())/2)
                self.layout.setContentsMargins(0,diff,0,diff)
            elif self.width() > self.height(): 
                diff = int((self.width() - self.height())/2)
                self.layout.setContentsMargins(diff,0,diff,0)
            else:
                self.layout.setContentsMargins(0,0,0,0)
        return super().resizeEvent(a0)


class QModeSwitch(QtWidgets.QFrame):
    def __init__(self, pixmapList):
        super(QModeSwitch, self).__init__()
        self.pixmapList = []
        for index in range(len(pixmapList)):
            if str(type(pixmapList[index])) == "<class 'str'>":
                self.pixmapList.append(QtGui.QPixmap.fromImage(QtGui.QImage(pixmapList[index])))
            elif str(type(pixmapList[index])) == "<class 'PyQt5.QtGui.QImage'>":
                self.pixmapList.append(QtGui.QPixmap.fromImage(pixmapList[index]))
            elif str(type(pixmapList[index])) == "<class 'PyQt5.QtGui.QPixmap'>":
                self.pixmapList.append(pixmapList[index])
            else:
                raise TypeError("QGoodButton(self, pixmapList): The 'pixmapList["+index+"]' parameter supplied to 'QGoodButton()' isn't a string, QImage, or a QPixmap - what the fuck are you importing?")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.layout)
        self.label = QtWidgets.QLabel()
        self.layout.addWidget(self.label)
        self.layout.setContentsMargins(0,0,0,0)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Ignored,QtWidgets.QSizePolicy.Ignored)
        self.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.label.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.label.setPixmap(self.pixmapList[0])
        self.label.setScaledContents(True)
        self.setMinimumSize(8,8)
        self.mode = 0
        self.maintainAspectRatio = True
        self.clicked = 0
    def clickedConnect(self, funcname):
        self.clicked = funcname
    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken) 
        return super().mousePressEvent(ev)
    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.mode += 1
        if self.mode == len(self.pixmapList): self.mode = 0
        self.clicked()
        self.label.setPixmap(self.pixmapList[self.mode])
        return super().mousePressEvent(ev)
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        if self.maintainAspectRatio:
            #Setting up the margins to maintain the aspect ratio
            if self.width() < self.height():
                diff = int((self.height() - self.width())/2)
                self.layout.setContentsMargins(0,diff,0,diff)
            elif self.width() > self.height(): 
                diff = int((self.width() - self.height())/2)
                self.layout.setContentsMargins(diff,0,diff,0)
            else:
                self.layout.setContentsMargins(0,0,0,0)
        return super().resizeEvent(a0)