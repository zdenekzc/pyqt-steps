#! /usr/bin/env python

from PyQt5.QtDBus import *

connection = QDBusConnection.sessionBus()

ifc = QDBusInterface ("org.example.receiver", "/org/example/ReceiverObject", "", connection)

msg = ifc.call ("hello", "Hello form script (using QtDBus)")

reply = QDBusReply (msg)
# see http://gitpress.io/u/1155/pyqt-example-ping

if reply.isValid () :
   answer = reply.value ()
   print ("answer is:", answer)




