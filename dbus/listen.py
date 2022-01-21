#! /usr/bin/env python

import dbus
import dbus.service
import dbus.mainloop.glib

from gi.repository import GLib

class SomeObject(dbus.service.Object):

    #@dbus.service.method ("org.example.ReceiverInterface",
                          #in_signature='s',
                          #out_signature='s')
    @dbus.service.method ("org.example.ReceiverInterface")
    def hello (self, hello_message) :
        print ("Hello called with parameter:", str (hello_message))
        return "Hello from server (" +   hello_message + ")"

    @dbus.service.method ("org.example.ReceiverInterface")
    def navigateToSlot (self, objectName, signalSignature, parameterNames) :
        names =  [ str (item) for item in parameterNames ]
        print ("navigateToSlot", objectName, signalSignature, str (names))
        return None

if __name__ == '__main__':

    dbus_loop = dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    session_bus = dbus.SessionBus (mainloop=dbus_loop)
    name = dbus.service.BusName ("org.example.receiver", session_bus)
    object = SomeObject (session_bus, "/org/example/ReceiverObject")

    loop = GLib.MainLoop()
    print ("Running example service.")
    loop.run()

# archlinux: pacman -S dbus-python
