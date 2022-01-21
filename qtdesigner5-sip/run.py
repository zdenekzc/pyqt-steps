#! /usr/bin/env python

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# from PyQt5.QtDesigner import *

import sys
import designer

import dbus

class Window (QMainWindow) :

   @pyqtSlot ("QString", "QString", "QStringList")
   def navigateToSlot (self, objectName, signalSignature, parameterNames) :
       self.info.append ("NAVIGATE TO SLOT " + objectName + " " +  signalSignature + " " + str (parameterNames))
      
       bus = dbus.SessionBus ()
       remote_object = bus.get_object ("org.example.receiver", "/org/example/ReceiverObject")
       ifc = dbus.Interface (remote_object, "org.example.ReceiverInterface")
       names = [ str (item) for item in parameterNames ]
       if len (names) == 0 :
          names = [ "" ]
       ifc.navigateToSlot (str (objectName), str (signalSignature), names)

   def __init__ (self, parent = None) :
       super (Window, self).__init__ (parent)

       design = designer.Designer (self) # <-- PyQt5: self, otherwise drag and drop is not working, PyQt4 : parent, not self
       design.connectNavigation (self)

       info = QTextEdit (self)
       self.info = info

       left = QTabWidget (self)
       right = QTabWidget (self)

       left.addTab (design.widgetBox (), "widgets")
       left.addTab (design.objectInspector (), "objects")

       right.addTab (design.propertyEditor (), "properties")
       right.addTab (design.actionEditor (), "actions")

       right.addTab (design.resourceEditor (), "resources")
       right.addTab (design.signalSlotEditor (), "signals/slots")

       hsplitter = QSplitter (self)
       hsplitter.addWidget (left)
       hsplitter.addWidget (design.getForm ())
       hsplitter.addWidget (right)

       hsplitter.setStretchFactor (0, 10)
       hsplitter.setStretchFactor (1, 10)
       hsplitter.setStretchFactor (2, 10)

       vsplitter = QSplitter (self)
       vsplitter.setOrientation (Qt.Vertical)
       vsplitter.addWidget (hsplitter)
       vsplitter.addWidget (info)

       vsplitter.setStretchFactor (0, 30)
       vsplitter.setStretchFactor (1, 10)

       self.setCentralWidget (vsplitter)

       design.open ("example.ui")

app = QApplication (sys.argv)
win = Window ()

win.show ()
app.exec_ ()

if 0 :
   def showObject (obj, level) :
       print ("   " * level, obj.objectName(), ":" ,  obj.metaObject().className ())
       for c in obj.children() :
          showObject (c, level+1)

   for w in app.allWindows() :
       showObject (w, 1)
   for w in app.topLevelWindows() :
       showObject (w, 1)

   showObject (app, 1)
   showObject (win, 1)
   # print (win.children ())
