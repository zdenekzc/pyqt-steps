import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def variant_to_str (v) :
    if sys.version_info >= (3, 0) :
       return v
    else :
       v.toString ()

def bytes_to_str (data) :
    if sys.version_info >= (3, 0) :
        return str (data, "latin1")
    else:
        return str (data)

class Window (QMainWindow) :

    def __init__ (self, parent = None) :
       super (Window, self).__init__ (parent)

       self.tree = QTreeWidget ()
       self.tree.itemDoubleClicked.connect (self.itemClick)

       self.tab = QTabWidget ()

       splitter = QSplitter (self)
       splitter.addWidget (self.tree)
       splitter.addWidget (self.tab)
       self.setCentralWidget (splitter)

       self.displayDir (self.tree, "..")

    def displayDir (self, target, path) :
        localDir = QDir (path)
        directory = QDir (localDir.absolutePath ())
        item = QTreeWidgetItem (target)
        item.setText (0, directory.dirName ())
        item.setToolTip (0, directory.absolutePath ())
        item.setData (0, Qt.UserRole, directory.absolutePath ())
        item.setForeground (0, QColor ("red"))

        infoList = directory.entryInfoList (QDir.Files | QDir.Dirs |
                                            QDir.NoDotAndDotDot)
        for info in infoList :
            if info.isDir () :
               self.displayDir (item, info.filePath ())
            else :
               node = QTreeWidgetItem (item)
               node.setText (0, info.fileName ())
               node.setToolTip (0, info.filePath ())
               node.setData (0, Qt.UserRole, info.filePath ())
               node.setForeground (0, QColor ("blue"))

    def itemClick (self, item, column) :
        path = variant_to_str (item.data (0, Qt.UserRole))
        info = QFileInfo (path)
        ext = "." + info.completeSuffix ()
        widget = None

        if ext in [ ".h", ".cpp", ".py" ] :
           widget = QTextEdit ()
           f = QFile (path)
           if f.open (QFile.ReadOnly) :
              data = bytes_to_str (f.readAll ())
              widget.setText (data)

        if widget != None :
           self.tab.addTab (widget, info.fileName ())

if __name__ == "__main__" :
   app = QApplication (sys.argv)
   win = Window ()
   win.show ()
   app.exec_ ()
