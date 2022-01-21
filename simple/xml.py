import os, sys

from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *

class Window (QMainWindow) :
    def __init__ (self) :
        super (Window, self).__init__ ()

        self.tree = QTreeWidget ()
        self.setCentralWidget (self.tree)

        # self.scanXml ("plant_catalog.xml")
        # https://www.w3schools.com/XML/plant_catalog.xml

        manager = QNetworkAccessManager (self)
        manager.finished.connect (self.replyFinished)

        request = QNetworkRequest ()
        request.setUrl (QUrl ("https://www.w3schools.com/XML/plant_catalog.xml"))

        reply = manager.get (request)

    def replyFinished (self, reply) :
        print ("replyFinished")
        answer = reply.readAll ()
        self.scanXmlData (answer)

    def scanXmlFile (self, fileName) :
        f = QFile (fileName)
        if f.open (QFile.ReadOnly) :
           self.scan (f)

    def scanXmlData (self, data) :
        f = QBuffer (data)
        if f.open (QFile.ReadOnly) :
           self.scan (f)

    def scan (self, stream) :
        r = QXmlStreamReader (stream)
        target = self.tree
        while not r.atEnd () :
            if r.isStartElement() :
                node = QTreeWidgetItem (target)
                node.setText (0, r.name())
                target = node
            if r.isEndElement() :
                target = target.parent ()
            if r.isCharacters () :
                t = r.text().strip()
                if t != "" :
                   node = QTreeWidgetItem (target)
                   node.setText (0, t)
            r.readNext ()

if __name__ == "__main__" :
   appl = QApplication (sys.argv)
   win = Window ()
   win.show ()
   appl.exec_ ()
