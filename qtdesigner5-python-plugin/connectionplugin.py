#!/usr/bin/env python

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import dbus

from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from connectionwidget import ConnectionWidgetPyQt

class ConnectionPlugin (QPyDesignerCustomWidgetPlugin) :

    def __init__(self, parent=None):
        super (ConnectionPlugin, self).__init__(parent)
        self.initialized = False
        self.core = None
        self.message = ""

    def initialize (self, core):
        self.core = core
        if not self.initialized:
            self.initialized = True
            self.message = "initialized"
            self.core.parent().initialized.connect (self.setup)

    def setup (self) :
        self.message = "setup"
        obj = self.core.parent ()
        for item in obj.findChildren (QObject, "", Qt.FindDirectChildrenOnly) :
           name = item.metaObject().className ()
           if name == "QDesignerIntegration" :
              value = hasattr (item, "setFeatures")
              if value :
                 integration = item
                 typ = integration.metaObject ()
                 inx = typ.indexOfMethod ("setFeatures(Feature)")
                 meth = typ.method (inx)
                 self.message = self.message + str (meth.name ()) + ", " + str (meth.methodSignature ()) + "\n"
                 arg = Q_ARG (int, 2)
                 meth.invoke (integration, arg)
                 self.message = "complete"

                 # integration.navigateToSlot.connect (self.navigateToSlot)
                 self.integration = integration
                 integration.setObjectName ("integration")
                 integration.setParent (self)
                 QMetaObject.connectSlotsByName (self)
                 self.message = "ready"

    @pyqtSlot ("QString", "QString", "QStringList") 
    def on_integration_navigateToSlot (self, objectName, signalSignature, parameterNames) :
        self.message = "navigate"
        bus = dbus.SessionBus ()
        remote_object = bus.get_object ("org.example.receiver", "/org/example/ReceiverObject")
        ifc = dbus.Interface (remote_object, "org.example.ReceiverInterface")
        if len (parameterNames) == 0 :
           parameterNames = [ "" ]
        ifc.navigateToSlot (objectName, signalSignature, parameterNames)
        # ifc.hello (signalSignature)
        self.message = "sent"

    def isInitialized (self) :
        return self.initialized

    def createWidget (self, parent):
        widget = ConnectionWidgetPyQt (parent)
        widget.setText (self.message)
        return widget

    def name(self) :
        return "ConnectionWidgetPyQt"

    def group (self) :
        return "Designer Connection"

    def icon (self) :
        return QIcon ()

    def toolTip (self) :
        return "Qt Designer plugin with DBus connection (PyQt5)"

    def whatsThis (self) :
        return ""

    def isContainer (self) :
        return False

    def domXml (self) :
        return '<widget class="ConnectionWidgetPyQt" name="connectionWidget">\n' \
               '</widget>\n'

    def includeFile (self) :
        return "designerconnection"
