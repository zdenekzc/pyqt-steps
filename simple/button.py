import sys
from PyQt5.QtWidgets import *

class Window (QMainWindow) :

    def __init__ (self) :
        super().__init__()
        self.button = QPushButton (self)
        self.button.setText ("Button")
        self.button.clicked.connect (self.onClick)
        self.setCentralWidget (self.button)

    def onClick (self) :
        self.button.setText ("Click")

def main () :
    app = QApplication (sys.argv)
    win = Window ()
    win.show ()
    sys.exit (app.exec_())

if __name__ == "__main__" :
    main ()
