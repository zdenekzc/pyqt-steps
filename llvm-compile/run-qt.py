#!/bin/env python

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
app = QApplication (sys.argv)

import faulthandler
faulthandler.enable ()

import os
opts = os.popen ("pkg-config Qt5Core Qt5Gui Qt5Widgets --cflags").read().split ()

import compiler
comp = compiler.Compiler ()
# opts = opts + [ "-g" ] # line numbers
# opts = opts + [ "-rdynamic" ]
opts = opts + [ "sample-qt.cc" ]

libs = [
         "/usr/lib64/libstdc++.so.6",
         "/usr/lib64/libQt5Core.so",
         "/usr/lib64/libQt5Gui.so",
         "/usr/lib64/libQt5Widgets.so",
       ]

comp.compile (opts, libs)

# win = QPushButton()
# win.setText ("run-qt.py ")
# win.show ()
app.exec_()
