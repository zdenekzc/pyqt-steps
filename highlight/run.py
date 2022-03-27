#!/bin/env python

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys
import highlight

class Window (QTextEdit) :

   def __init__ (self, parent = None) :
       super (Window, self).__init__ (parent)
       self.highlighter = highlight.Highlighter (self.document ()) # important: keep reference to highlighter

       text = """
          int main (int argc, char * * argv)
          {
             QString s = "abc";
             return 0;
          }
       """
       self.setText (text)

app = QApplication (sys.argv)
win = Window ()

win.show ()
app.exec_ ()
