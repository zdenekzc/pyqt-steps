import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ColorButton (QToolButton) :
    def __init__ (self, page, name, color) :
        super().__init__(page)
        self.name = name
        self.color = color

        self.setToolTip (name)
        page.addWidget (self)

        pixmap = QPixmap (12, 12)
        pixmap.fill (Qt.transparent)

        painter = QPainter (pixmap)
        painter.setPen (Qt.NoPen)
        painter.setBrush (color)
        painter.drawEllipse (0, 0, 12, 12)
        painter.end ()

        icon = QIcon (pixmap)
        self.setIcon (icon)

    def mousePressEvent (self, event) :

        drag = QDrag (self)

        mimeData = QMimeData ()
        mimeData.setText (self.name)
        mimeData.setColorData (self.color)

        drag.setMimeData (mimeData)

        drop = drag.exec_ ()

class Block (QGraphicsRectItem) :

    def __init__ (self) :
        super().__init__()
        self.setAcceptDrops (True)

    def dragEnterEvent (self, event) :
        mime = event.mimeData ()
        if mime.hasColor () :
           event.setAccepted (True)
        else :
           event.setAccepted (False)

    def dropEvent (self, event) :
        mime = event.mimeData ()
        if mime.hasColor () :
           color = mime.colorData ()
           self.setBrush (color)

class Window (QMainWindow) :

    def __init__ (self) :
        super().__init__()

        self.widget = QWidget ()
        self.setCentralWidget (self.widget)

        self.layout = QVBoxLayout (self.widget)

        self.palette = QTabWidget ()
        self.layout.addWidget (self.palette)

        self.colorPage = QToolBar ()
        self.palette.addTab (self.colorPage, "Colors")

        names = [ "red", "green", "blue", "yellow", "orange" ]
        for name in names :
            ColorButton (self.colorPage, name, QColor (name))

        self.toolPage = QToolBar ()
        self.palette.addTab (self.toolPage, "Tools")

        self.view = QGraphicsView ()
        self.layout.addWidget (self.view)

        self.scene = QGraphicsScene (self)
        self.view.setScene (self.scene)
        self.scene.setSceneRect (0, 0, 800, 600)

        # self.scene.addLine (0, 0, 200, 100, QColor ("red"))

        n = 16
        texture = QBitmap (n, n)
        texture.clear ()

        painter = QPainter (texture)
        painter.drawLine (0, 0, n-1, 0)
        painter.drawLine (0, 0, 0, n-1)
        painter.end ()

        brush = QBrush (QColor ("cornflowerblue"))
        brush.setTexture (texture)
        self.scene.setBackgroundBrush (brush)

        block = Block ()
        block.setRect (0, 0, 200, 120)
        block.setPos (100, 100)
        block.setPen (QColor ("blue"))
        block.setBrush (QColor ("yellow"))
        block.setToolTip ("block")
        block.setFlags (QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.scene.addItem (block)

        for i in range (2) :
            item = QGraphicsEllipseItem ()
            item.setRect (0, 0, 40, 40)
            item.setPos (40 + i*80, 40)
            item.setPen (QColor ("blue"))
            item.setBrush (QColor ("cornflowerblue"))
            item.setToolTip ("item " + str (i+1))
            item.setFlags (QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
            item.setParentItem (block)

app = QApplication (sys.argv)
win = Window ()
win.show ()
app.exec_()
