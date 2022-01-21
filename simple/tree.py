import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Window (QMainWindow) :

    def __init__ (self) :
        super().__init__ ()

        self.widget = QWidget (self)

        self.layout = QVBoxLayout (self.widget)

        self.setCentralWidget (self.widget)

        # self.setFont (QFont ("", 20))

        self.tree = QTreeWidget (self)
        self.tree.header().setVisible (False)
        self.layout.addWidget (self.tree)

        self.button = QPushButton (self)
        self.button.setText ("Add Items")
        self.button.clicked.connect (self.onClick)

        self.layout.addWidget (self.button)

    def onClick (self) :

        branch = QTreeWidgetItem (self.tree)
        branch.setText (0, "abc")
        branch.setForeground (0, QColor ("brown"))
        branch.setExpanded (True)

        colors = [ "red", "blue", "green", "yellow", "orange"]
        for name in colors :
           item = QTreeWidgetItem (branch)
           item.setText (0, name + " item")
           item.setForeground (0, QColor (name))

if __name__ == "__main__" :
    app = QApplication (sys.argv)
    win = Window ()
    win.show ()
    win.raise_ ()
    sys.exit (app.exec_ ())
