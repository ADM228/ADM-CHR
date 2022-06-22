from PyQt5 import QtWidgets, QtGui, QtCore
class QGoodButton(QtWidgets.QFrame):
    def __init__(self, pixmap):
        super(QGoodButton, self).__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.layout)
        self.label = QtWidgets.QLabel()
        self.layout.addWidget(self.label)
        self.layout.setContentsMargins(0,0,0,0)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Ignored,QtWidgets.QSizePolicy.Ignored)
        self.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.label.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        self.setMinimumSize(8,8)
        self.maintainAspectRatio = True
    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        return super().mousePressEvent(ev)
    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
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
