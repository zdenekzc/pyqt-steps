import os, sys

from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg     import *
from PyQt5.QtNetwork import *

class Window (QMainWindow) :
    def __init__ (self) :
        super (Window, self).__init__ ()

        self.view = QSvgWidget ()
        self.setCentralWidget (self.view)

        # self.view.load ("Downloads/tiger.svg")
        manager = QNetworkAccessManager (self)
        manager.finished.connect (self.replyFinished)

        request = QNetworkRequest ()
        request.setUrl (QUrl ("https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/tiger.svg"))

        reply = manager.get (request)

    def replyFinished (self, reply) :
        print ("replyFinished")
        answer = reply.readAll ()
        self.view.load (answer)

if __name__ == "__main__" :
   appl = QApplication (sys.argv)
   win = Window ()
   win.show ()
   appl.exec_ ()

# http://doc.qt.io/qt-5/qnetworkaccessmanager.html
