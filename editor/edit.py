
from __future__ import print_function

import sys, subprocess

try :
   from PyQt5.QtCore import *
   from PyQt5.QtGui import *
   from PyQt5.QtWidgets import *
   print ("using PyQt5")
   use_qt5 = True
except :
   from PyQt4.QtCore import *
   from PyQt4.QtGui import *
   print ("using PyQt4")
   use_qt5 = False

# Windows: pip3 install PyQt5
# Debian, Ubuntu: apt-get install python3-pyqt5
# Fedora: dnf install python3-qt5
# ArchLinux: pacman -S python-pyqt5

# --------------------------------------------------------------------------

if sys.version_info >= (3,) :
   use_python3 = True
else :
   use_python3 = False

use_new_api = use_python3 or use_qt5

def dialog_to_str (s) :
    # get file name from open file dialog results
    if use_new_api :
       return s[0]
    else :
       return str (s)

def bytearray_to_str (b) :
    if use_python3 :
       return str (b, "ascii", errors="ignore")
    else :
       return str (b)

# --------------------------------------------------------------------------

class Window (QMainWindow) :

   def __init__ (self, parent = None) :
       super (Window, self).__init__ (parent)

       # variables

       self.fileName = ""

       # user interface

       self.edit = QTextEdit ()
       self.edit.setLineWrapMode (QTextEdit.NoWrap)

       self.output = QTextEdit ()

       splitter = QSplitter (self)
       splitter.addWidget (self.edit)
       splitter.addWidget (self.output)
       splitter.setOrientation (Qt.Vertical)
       splitter.setStretchFactor (0, 3)
       splitter.setStretchFactor (1, 1)

       self.setCentralWidget (splitter)

       # status bar

       ver = sys.version_info
       inf = str (ver[0]) + "." + str (ver[1]) + "." + str (ver[2])
       self.statusBar().showMessage ("Python " + inf + ", Qt " + qVersion ())

       # menu

       fileMenu = self.menuBar().addMenu ("&File")

       act = QAction ("&Open...", self)
       act.setShortcut ("Ctrl+O")
       act.triggered.connect (self.openFile)
       fileMenu.addAction (act)

       act = QAction ("&Save...", self)
       act.setShortcut ("Ctrl+S")
       act.triggered.connect (self.saveFile)
       fileMenu.addAction (act)

       act = QAction ("&Quit", self)
       act.setShortcut ("Ctrl+Q")
       act.triggered.connect (self.close)
       fileMenu.addAction (act)

       runMenu = self.menuBar().addMenu ("&Run")

       act = QAction ("&Compile and Run", self)
       act.setShortcut ("F5")
       act.triggered.connect (self.runFile)
       runMenu.addAction (act)

   def openFile (self) :
       self.fileName = dialog_to_str (QFileDialog.getOpenFileName (self, "Open File"))
       if self.fileName != "" :
          f = open (self.fileName)
          text = f.read ()
          self.edit.setPlainText (text)
          self.setWindowTitle (self.fileName)

   def saveFile (self) :
       self.fileName = dialog_to_str (QFileDialog.getSaveFileName (self, "Save File As", self.fileName))
       if self.fileName != "" :
          text = self.edit.toPlainText ()
          f = open (self.fileName, "w")
          f.write (text)
          self.setWindowTitle (self.fileName)

   def runFile (self) :
       if self.fileName != "" :
          self.output.clear ()
          cmd = "gcc " + self.fileName + " -lstdc++ -o run.bin && ./run.bin && rm ./run.bin"
          self.output.append (cmd)
          proc = subprocess.Popen (cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
          for line in proc.stderr :
              self.output.append (bytearray_to_str (line))
          for line in proc.stdout :
              self.output.append (bytearray_to_str (line))

if __name__ == "__main__" :
   app = QApplication (sys.argv)
   win = Window ()
   win.show ()
   app.exec_ ()
