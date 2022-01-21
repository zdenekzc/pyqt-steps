#! /usr/bin/env python

import dbus, sys

bus = dbus.SessionBus ()

remote_object = bus.get_object ("org.example.receiver", "/org/example/ReceiverObject")

ifc = dbus.Interface (remote_object, "org.example.ReceiverInterface")

answer = ifc.hello ("Hello form script")

print ("answer is:", answer)

# dnf install qt5-qdbusviewer
# qdbusviewer-qt5

# dnf install qt-qdbusviewer
# qdbusviewer




