import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Widget (QWidget) :

    def __init__ (self) :
        super().__init__()

    def color (self, painter, r, g, b) :
        painter.setPen (QColor.fromRgb (r, g, b))

    def line (self, painter, x1, y1, x2, y2) :
        painter.drawLine (x1, y1, x2, y2)

    def paintEvent (self, event) : # QPaintEvent *event
        p = QPainter ()
        p.begin (self)

        w = self.width ()
        h = self.height ()

        self.color (p, 255, 0, 0)
        self.line  (p, 0, 0, w-1, 0)

        self.color (p, 0, 255, 0)
        self.line  (p, w-1, 0, w-1, h-1)

        self.color (p, 0, 0, 255)
        self.line  (p, w-1, h-1, 0, h-1)

        self.color (p, 255, 200, 0)
        self.line  (p, 0, h-1, 0, 0)

        p.end ()

if __name__ == "__main__" :
    app = QApplication (sys.argv)
    win = Widget ()
    win.show ()
    sys.exit (app.exec_())
