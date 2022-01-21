import sys, subprocess

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# --------------------------------------------------------------------------


def dialog_to_str (s) :
    # get file name from open file dialog results
    return s[0]

def bytearray_to_str (b) :
    return str (b, "ascii", errors="ignore")

# --------------------------------------------------------------------------

def isLetter (c) :
    return c >= 'A' and c <= 'Z' or c >= 'a' and c <= 'z' or c == '_'

def isDigit (c) :
    return c >= '0' and c <= '9'

def isLetterOrDigit (c) :
    return c >= 'A' and c <= 'Z' or c >= 'a' and c <= 'z' or c == '_' or c >= '0' and c <= '9'

class Highlighter (QSyntaxHighlighter) :

   def __init__ (self, parent = None) :
       super (Highlighter, self).__init__ (parent)

       self.keywordFormat = QTextCharFormat ()
       self.keywordFormat.setForeground (QColor ("darkRed"))

       self.identifierFormat = QTextCharFormat ()
       self.identifierFormat.setForeground (QColor ("darkBrown"))

       self.qidentifierFormat = QTextCharFormat ()
       self.qidentifierFormat.setForeground (QColor ("green"))

       self.numberFormat = QTextCharFormat ()
       self.numberFormat.setForeground (QColor ("lightBlue"))

       self.characterFormat = QTextCharFormat ()
       self.characterFormat.setForeground (QColor ("cornflowerblue"))

       self.stringFormat = QTextCharFormat ()
       self.stringFormat.setForeground (QColor ("blue"))

       self.commentFormat = QTextCharFormat ()
       self.commentFormat.setForeground (QColor ("gray"))

       self.keywords = ["if", "else", "for", "while", "return", "using", "namespace"];

   def highlightBlock (self, text) :
       cnt = len (text)
       inx = 0

       inside_comment = self.previousBlockState () == 1
       start_comment = 0

       while inx < cnt :
          if inside_comment :
             if inx == 0 :
                inx = 1
             while inx < cnt and (text [inx-1] != '*' or text [inx] != '/')  :
                inx = inx + 1
             if inx < cnt:
                inx = inx + 1
                self.setFormat (start_comment, inx-start_comment, self.commentFormat)
                inside_comment = False
          else :

             while inx < cnt and text [inx] <= ' ' :
                inx = inx + 1

             start = inx

             if inx < cnt :
                c = text [inx]

                if isLetter (c) :
                   name = ""
                   while inx < cnt and isLetterOrDigit (text [inx]) :
                      name = name + text [inx]
                      inx = inx + 1

                   if c == 'Q' :
                      self.setFormat (start, inx-start, self.qidentifierFormat)
                   elif name in self.keywords :
                      self.setFormat (start, inx-start, self.keywordFormat)
                   else :
                      self.setFormat (start, inx-start, self.identifierFormat)

                elif isDigit (c) :
                   while inx < cnt and isDigit (text [inx]) :
                      inx = inx + 1
                      self.setFormat (start, inx-start, self.numberFormat)

                elif c == '"' :
                   inx = inx + 1
                   while inx < cnt and text [inx] != '"' :
                      inx = inx + 1
                   inx = inx + 1
                   self.setFormat (start, inx-start, self.stringFormat)

                elif c == "'" :
                   inx = inx + 1
                   while inx < cnt and text [inx] != "'" :
                      inx = inx + 1
                   inx = inx + 1
                   self.setFormat (start, inx-start, self.characterFormat)

                elif c == '/' :
                   inx = inx + 1
                   if inx < cnt and text [inx] == '/' :
                      inx = cnt # end of line
                      self.setFormat (start, inx-start, self.commentFormat)
                   elif inx < cnt and text [inx] == '*' :
                      inx = inx + 1 # skip asterisk
                      inside_comment = True
                      start_comment = inx - 2 # back to slash

                else :
                   inx = inx + 1

       if inside_comment :
          self.setFormat (start_comment, inx-start_comment, self.commentFormat)
          self.setCurrentBlockState (1)
       else :
          self.setCurrentBlockState (0)

# --------------------------------------------------------------------------

class CompletionTextEdit (QTextEdit) :

   def __init__ (self, parent = None) :
       super (CompletionTextEdit, self).__init__ (parent)

       self.win = None
       self.completer = None

       self.minLength = 1
       self.automatic_completion = False
       # self.automatic_completion == False ... popup is displayed only when Ctrl+Space is pressed

       localList = [ ]
       localCompleter = QCompleter (localList, self)
       self.setCompleter (localCompleter, filtered = True)

   def setCompleter (self, completer, filtered = False) :
       if self.completer :
           # self.disconnect (self.completer, SIGNAL ("activated(const QString&)"),  self.insertCompletion)
           self.completer.activated.disconnect (self.insertCompletion)
       if completer == None :
           return

       completer.setWidget (self)

       if filtered :
          completer.setCompletionMode (QCompleter.PopupCompletion)
       else :
          completer.setCompletionMode (QCompleter.UnfilteredPopupCompletion)

       completer.setCaseSensitivity (Qt.CaseInsensitive)

       self.completer = completer
       # self.connect (self.completer, SIGNAL ("activated(const QString&)"), self.insertCompletion)
       self.completer.activated.connect (self.insertCompletion)

   def insertCompletion (self, completion) :
       if self.completer.widget() == self :
          tc = self.textCursor ()
          if use_new_api :
             extra = len (completion) -  len (self.completer.completionPrefix())
          else :
             extra = completion.length() -  self.completer.completionPrefix().length()
          if extra != 0 :
             tc.movePosition (QTextCursor.Left)
             tc.movePosition (QTextCursor.EndOfWord)
          if use_new_api :
             tc.insertText (completion [-extra : ])
          else :
             tc.insertText (completion.right (extra))
          self.setTextCursor (tc)

   def textUnderCursor (self) :
       tc = self.textCursor ()
       tc.select (QTextCursor.WordUnderCursor)
       return tc.selectedText ()

   def focusInEvent (self, event) :
       if self.completer :
           self.completer.setWidget (self);
       QTextEdit.focusInEvent (self, event)

   def focusOutEvent (self, event) :
       QTextEdit.focusOutEvent (self, event)

   def keyPressEvent (self, event) :
       if self.completer != None and self.completer.popup().isVisible() :
           if event.key () in (
              Qt.Key_Enter,
              Qt.Key_Return,
              Qt.Key_Escape,
              Qt.Key_Tab,
              Qt.Key_Backtab) :
                 event.ignore ()
                 return

       mask = Qt.ShiftModifier | Qt.ControlModifier | Qt.AltModifier | Qt.MetaModifier
       mod = int (event.modifiers () & mask)

       isShortcut = mod == Qt.ControlModifier and event.key () == Qt.Key_Space # Ctrl + Space

       if (self.completer == None or not isShortcut) :
           QTextEdit.keyPressEvent (self, event) # do not process the shortcut when we have a completer
           if not self.automatic_completion :
              return

       ctrlOrShift = mod in (Qt.ControlModifier, Qt.ShiftModifier)
       if self.completer == None or (ctrlOrShift and event.text () == "") : # unicode has not isEmpty method
           # ctrl or shift key on it's own
           return

       eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-=" # end of word
       if not use_new_api :
          eow = QString (eow)

       hasModifier = ((event.modifiers () != Qt.NoModifier) and not ctrlOrShift)

       # completionList = [ ]
       completionList = self.getCompletionList ()
       model = QStringListModel (completionList, self.completer)
       self.completer.setModel (model)

       completionPrefix = self.textUnderCursor ()

       if use_new_api :
          if (not isShortcut
              and (hasModifier or
                   event.text () == "" or
                   len (completionPrefix) < self.minLength or
                   event.text()[-1] in eow )) :
              self.completer.popup ().hide ()
              return
       else :
          if (not isShortcut
              and (hasModifier or
                   event.text ().isEmpty () or
                   completionPrefix.length () < self.minLength or
                   eow.contains (event.text().right(1)) )) :
              self.completer.popup ().hide ()
              return

       if (completionPrefix != self.completer.completionPrefix ()) :
           self.completer.setCompletionPrefix (completionPrefix)
           popup = self.completer.popup ()
           popup.setCurrentIndex (self.completer.completionModel ().index (0,0))

       cr = self.cursorRect ()
       cr.setWidth (self.completer.popup ().sizeHintForColumn (0) +
                    self.completer.popup ().verticalScrollBar ().sizeHint ().width ())
       self.completer.complete (cr) # popup it

   def getCompletionList (self) :
       return [ "alpha", "beta", "gamma" ]

# http://doc.qt.io/qt-5/qtwidgets-tools-customcompleter-example.html
# http://rowinggolfer.blogspot.cz/2010/08/qtextedit-with-autocompletion-using.html

# --------------------------------------------------------------------------

class Window (QMainWindow) :

   def __init__ (self, parent = None) :
       super (Window, self).__init__ (parent)

       # variables

       self.fileName = ""

       # user interface

       self.edit = CompletionTextEdit ()
       self.edit.setLineWrapMode (QTextEdit.NoWrap)
       self.highlighter = Highlighter (self.edit.document ()) # important: keep reference to highlighter

       self.output = QTextEdit ()
       self.output.setLineWrapMode (QTextEdit.NoWrap)

       splitter = QSplitter (self)
       splitter.addWidget (self.edit)
       splitter.addWidget (self.output)
       splitter.setOrientation (Qt.Vertical)
       splitter.setStretchFactor (0, 3)
       splitter.setStretchFactor (1, 1)

       self.setCentralWidget (splitter)

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

       editMenu = self.menuBar().addMenu ("&Edit")

       act = QAction ("set &Font", self)
       act.triggered.connect (self.selectFont)
       editMenu.addAction (act)

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

   def selectFont (self) :
       font, ok = QFontDialog.getFont (self.edit.currentFont (), self)
       if ok :
          self.edit.setFont (font)
          self.output.setFont (font)

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

# --------------------------------------------------------------------------

if __name__ == "__main__" :
   app = QApplication (sys.argv)
   win = Window ()
   win.show ()
   app.exec_ ()
