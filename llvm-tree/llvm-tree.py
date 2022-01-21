#!/usr/bin/env python

from __future__ import print_function

import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

sys.path.append (os.path.expanduser ("/abc/llvm-python"))
# directory with clang/cindex.py

import clang.cindex
from clang.cindex import Index, Config, CursorKind

# clang.cindex.Config.set_library_path ("/usr/lib/llvm")
# clang.cindex.Config.set_library_file ("/usr/lib/llvm/libclang.so")

# --------------------------------------------------------------------------

def findIcon (icon_name):
    icon = QIcon.fromTheme (icon_name)
    return icon

class TreeItem (QTreeWidgetItem):
    def __init__ (self, parent, text):
        QTreeWidgetItem.__init__ (self, parent)
        self.setText (0, text)

    def addIcon (self, icon_name):
        self.setIcon (0, findIcon (icon_name))

class TreeView (QTreeWidget):
    def __init__ (self, parent=None):
        QTreeWidget.__init__ (self, parent)
        self.setColumnCount (1)
        self.header ().hide ()
        # self.setRootIsDecorated (True)
        # self.setSelectionMode (QAbstractItemView.ExtendedSelection)
        self.setEditTriggers (QAbstractItemView.SelectedClicked)
        self.setIndentation (8);

# --------------------------------------------------------------------------

class MainWin (QMainWindow):

    def __init__ (self, parent=None):
        QMainWindow.__init__ (self, parent)
        self.translation_unit = None
        self.translation_cursor = None
        self.setupUI ()
        self.setupMenus ()
        self.setupConnections ()

    def setupUI (self) :
        self.setStatusBar (QStatusBar ())
        self.resize (640, 480);

        self.split = QSplitter ()
        self.setCentralWidget (self.split)

        self.treeView = TreeView ()
        self.split.addWidget (self.treeView)

        self.rightTabs = QTabWidget ()
        self.rightTabs.tabBar().setFocusPolicy (Qt.NoFocus)
        self.rightTabs.setTabPosition (QTabWidget.South)
        self.split.addWidget (self.rightTabs)

        self.editors = { }

    def action (self, name, icon_image = None ) :
        title = name.title ()
        act = QAction ("&" + title, self)
        if icon_image :
           act.setIcon (icon_image)
        return act

    def setupMenus (self):

        fileMenu = self.menuBar().addMenu ("&File")

        # act = self.action ("Open...")
        # self.connect (act, click, self.openFile)
        # fileMenu.addAction (act)

        act = self.action ("Quit")
        act.triggered.connect (self.close)
        fileMenu.addAction (act)

        editMenu = self.menuBar().addMenu ("&Edit")

        act = self.action ("Complete")
        act.triggered.connect (self.complete)
        editMenu.addAction (act)

    def setupConnections (self):

        self.treeView.itemClicked.connect (self.treeView_itemClicked)

    def complete (self):
        if self.translation_unit != None :

           fileName = ""
           edit = self.rightTabs.currentWidget ()
           for name in self.editors :
               if self.editors [name] == edit :
                  fileName = name

           cursor = edit.textCursor ()
           line = cursor.blockNumber () + 1
           column = cursor.positionInBlock () + 1

           print (fileName, str (line), str (column))

           answer = self.translation_unit.codeComplete (fileName, line, column,
                                                        unsaved_files=None,
                                                        include_macros=False,
                                                        include_code_patterns=False,
                                                        include_brief_comments=False)
           if answer != None :
              for t in answer.results :
                 print (t)

    def treeView_itemClicked (self, tree_node, column) :
        txt = ""
        if hasattr (tree_node, "fileName") :
           txt = tree_node.fileName + ", line: " + str (tree_node.line) + ", column: " + str (tree_node.column)
           self.openSource (tree_node.fileName, tree_node.line, tree_node.column, tree_node.stop_line, tree_node.stop_column)
        self.statusBar().showMessage(txt)

    def openSource (self, fileName, line, col, stop_line, stop_col):
        if fileName not in self.editors :

           view = QTextEdit ()
           view.setLineWrapMode (QTextEdit.NoWrap)

           name = os.path.basename (fileName)
           self.rightTabs.addTab (view, name)
           self.editors[fileName] = view

           try :
              text = open(fileName).read()
              view.setText (text)
           except :
              pass

        edit = self.editors[fileName]
        self.rightTabs.setCurrentWidget (edit)

        cursor = edit.textCursor ()

        if 1 :
           cursor.movePosition (QTextCursor.Start)
           cursor.movePosition (QTextCursor.Down, QTextCursor.MoveAnchor, line-1)
           cursor.movePosition (QTextCursor.Right, QTextCursor.MoveAnchor, col-1)

           if stop_line >= 0 and stop_col >= 0 :
               if stop_line == line :
                  cursor.movePosition (QTextCursor.Right, QTextCursor.KeepAnchor, stop_col-col)
               else :
                  cursor.movePosition (QTextCursor.Down, QTextCursor.KeepAnchor, stop_line-line)
                  cursor.movePosition (QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
                  cursor.movePosition (QTextCursor.Right, QTextCursor.KeepAnchor, stop_col)

        if 0 :
           if stop_line >= 0 and stop_col >= 0 :
                  cursor.movePosition (QTextCursor.Start)
                  cursor.movePosition (QTextCursor.Down, QTextCursor.MoveAnchor, stop_line-1)
                  cursor.movePosition (QTextCursor.Right, QTextCursor.MoveAnchor, stop_col-1)

                  if stop_line == line :
                     cursor.movePosition (QTextCursor.Left, QTextCursor.KeepAnchor, stop_col-col)
                  else :
                     cursor.movePosition (QTextCursor.Up, QTextCursor.KeepAnchor, stop_line-line)
                     cursor.movePosition (QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
                     cursor.movePosition (QTextCursor.Right, QTextCursor.KeepAnchor, col)
           else :
              cursor.movePosition (QTextCursor.Start)
              cursor.movePosition (QTextCursor.Down, QTextCursor.MoveAnchor, line-1)
              cursor.movePosition (QTextCursor.Right, QTextCursor.MoveAnchor, col-1)

        edit.setTextCursor (cursor)

    # def openFile (self) :
    #     fileName = QFileDialog.getOpenFileName (self, "Open File")
    #     if fileName :
    #        self.translateFile (str (fileName))

    def translate (self, args) :
        top = TreeItem (self.treeView, "translation unit")
        top.addIcon  ("text-plain");

        index = clang.cindex.Index.create()
        tu = index.parse (None, args)
        if tu :
           # tu.reparse ()
           self.translation_cursor = index # important, keep index
           self.translation_unit = tu
           self.addBranch (top, tu.cursor, 10);

        top.setExpanded (True)

    def addBranch (self, above, node, level):
        txt = str (node.kind).replace ("CursorKind.", "", 1)
        txt = txt + ": " + str (node.spelling)
        item = TreeItem (above, txt)

        if (node.kind == CursorKind.CLASS_DECL or
            node.kind == CursorKind.STRUCT_DECL or
            node.kind == CursorKind.UNION_DECL) :
                item.addIcon ("code-class")
        elif (node.kind == CursorKind.FUNCTION_DECL or
              node.kind == CursorKind.CXX_METHOD or
              node.kind == CursorKind.CONSTRUCTOR or
              node.kind == CursorKind.DESTRUCTOR) :
                 item.addIcon ("code-function")
        elif (node.kind == CursorKind.VAR_DECL or
              node.kind == CursorKind.PARM_DECL or
              node.kind == CursorKind.FIELD_DECL) :
                 item.addIcon ("code-variable")

        item.location = node.location
        item.start = node.extent.start
        item.stop = node.extent.end

        start = item.start
        stop = item.stop

        if hasattr (start, "file") and hasattr (start.file, "name"):
           pass
        else :
           start = item.location

        if hasattr (start, "file") and hasattr (start.file, "name"):
           item.fileName = start.file.name
           item.line = start.line
           item.column = start.column
           if item.stop.file != None and item.fileName == stop.file.name :
              item.stop_line = stop.line
              item.stop_column = stop.column
           else :
              item.end_line = -1
              item.end_column = -1

        # item.setToolTip (0, QString (str (item.start) + str (item.location) + str (item.stop)))
        item.setToolTip (0, str (item.location))

        if level > 1 :
           for t in node.get_children() :
               self.addBranch (item, t, level-1)

# --------------------------------------------------------------------------

QIcon.setThemeName ("oxygen")

app = QApplication ([""])

win = MainWin ()
win.show ()
win.translate (sys.argv [ 1 : ])

app.exec_ ()

# --------------------------------------------------------------------------

# kate: indent-width 1; show-tabs true; replace-tabs true; remove-trailing-spaces all
