import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def bytes_to_str (b) :
    return str (b, "ascii", errors="ignore")

class StructWin (QTreeWidget):

    def __init__ (self, parent=None) :
        super (StructWin, self).__init__ (parent)

    def display (self, name, data) :
        node = QTreeWidgetItem ()
        node.setText (0, name)
        node.setForeground (0, QColor ("orange"))
        self.addTopLevelItem (node)

        self.displayProperties (node, data)
        self.displaySignals (node, data)
        self.displaySlots (node, data)
        self.displayMethods (node, data)

        node.setExpanded (True)

    def displayProperties (self, target, data) :
        branch = QTreeWidgetItem ()
        branch.setText (0, "properties")
        branch.setForeground (0, QColor (0, 0, 255))
        target.addChild (branch)

        typ = data.metaObject ()
        cnt = typ.propertyCount ()
        for inx in range (cnt) :
            prop = typ.property (inx)
            value = str (prop.read (data))
            txt = prop.name () + " : " + prop.typeName () + " = " + value
            node = QTreeWidgetItem ()
            node.setText (0, txt)
            node.setForeground (0, QColor (0, 0, 255))
            branch.addChild (node)

    def displaySignals (self, target, data) :
        branch = QTreeWidgetItem ()
        branch.setText (0, "signals")
        branch.setForeground (0, QColor (0, 255, 0))
        target.addChild (branch)

        typ = data.metaObject ()
        cnt = typ.methodCount ()
        for inx in range (cnt) :
            method = typ.method (inx)
            if method.methodType () == QMetaMethod.Signal :
               node = QTreeWidgetItem ()
               node.setText (0, bytes_to_str (method.methodSignature ()))
               node.setForeground (0, QColor (0, 255, 0))
               branch.addChild (node)

    def displaySlots (self, target, data) :
        branch = QTreeWidgetItem ()
        branch.setText (0, "slots")
        branch.setForeground (0, QColor (0, 255, 0))
        target.addChild (branch)

        typ = data.metaObject ()
        cnt = typ.methodCount ()
        for inx in range (cnt) :
            method = typ.method (inx)
            if method.methodType () == QMetaMethod.Slot :
               node = QTreeWidgetItem ()
               node.setText (0, bytes_to_str (method.methodSignature ()))
               node.setForeground (0, QColor (0, 255, 0))
               branch.addChild (node)

    def displayMethods (self, target, data) :
        branch = QTreeWidgetItem ()
        branch.setText (0, "methods")
        branch.setForeground (0, QColor (255, 0, 0))
        target.addChild (branch)

        typ = data.metaObject ()
        cnt = typ.methodCount ()
        for inx in range (cnt) :
            method = typ.method (inx)
            if method.methodType () != QMetaMethod.Method :
               node = QTreeWidgetItem ()
               node.setText (0, bytes_to_str (method.methodSignature ()))
               node.setForeground (0, QColor (255, 0, 0))
               branch.addChild (node)

if __name__ == '__main__' :
   app = QApplication (sys.argv)
   win = StructWin ()
   win.show ()
   win.display ("window", win)
   app.exec_ ()
