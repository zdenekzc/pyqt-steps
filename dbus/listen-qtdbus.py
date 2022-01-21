#! /usr/bin/env python

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtDBus import *

def qstringlist_to_list (obj) :
    if use_new_api :
       return obj
    else :
       return [ str (item) for item in obj ]


class Listener (QDBusAbstractAdaptor) :
   Q_CLASSINFO('D-Bus Interface', 'org.example.ReceiverInterface')

   def __init__ (self, win) :
       super (Listener, self).__init__ (win)
       self.win = win
       QDBusConnection.sessionBus().registerObject ("/org/example/ReceiverObject", win)

       if not QDBusConnection.sessionBus().registerService ("org.example.receiver") :
          print (QDBusConnection.sessionBus().lastError().message())

   @pyqtSlot ("QString", result = "QString")
   def hello (self, hello_message) :
       print ("Hello called with parameter:", str (hello_message))
       self.win.append ("Hello called with parameter:" + str (hello_message) + "\n")
       return "Hello from listen-qtdbus (" +   hello_message + ")"

   @pyqtSlot ("QString", "QString", "QStringList")
   def navigateToSlot (self, objectName, signalSignature, parameterNames) :
       # parameterNames = [ str (item) for item in parameterNames ]
       print ("NAVIGATE TO SLOT " + objectName + " " +  signalSignature + " " + str (parameterNames))
       self.win.append ("NAVIGATE TO SLOT " + objectName + " " +  signalSignature + " " + str (parameterNames) + "\n")

app = QApplication (sys.argv)
win = QTextEdit ()
win.setWindowTitle ("listen-qdbus.py")
win.show ()
listener = Listener (win)
app.exec ()


