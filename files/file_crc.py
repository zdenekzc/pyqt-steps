import os, sys, time, hashlib
from stat import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def size_str (n) :
    s = str (n)
    while len (s) < 9 :
        s = " " + s
    s = s[0:3] + " " + s[3:6] + " " + s[6:]
    return s

class Window (QMainWindow) :

    def __init__ (self) :
        super().__init__()

        self.widget = QWidget ()
        self.setCentralWidget (self.widget)

        self.layout = QVBoxLayout (self.widget)

        self.tree = QTreeWidget (self)
        self.tree.setHeaderLabels(["name", "size", "date", "crc"])
        self.layout.addWidget (self.tree)

        path = ".."
        root = self.tree.invisibleRootItem ()
        self.start (root, path)
        # self.check (root, path)

    def start (self, target, dir_path) :
        subitems = os.listdir (dir_path)
        subitems.sort ()
        for name in subitems :
            node = QTreeWidgetItem ()
            node.setText (0, name)
            target.addChild (node)

            path = os.path.join (dir_path, name)
            node.name = name
            node.path = path

            if os.path.isdir (path) :
                node.setForeground  (0, QColor ("orange"))
                self.start (node, path)
            else :
                node.setForeground  (0, QColor ("blue"))

                # import os, sys, time, hashlib
                # from stat import *
                try :
                    info = os.stat (path)
                    size = info [ST_SIZE]
                    node.setText (1, size_str (size))

                    t = info [ST_MTIME]
                    t = time.gmtime (t)
                    s = time.strftime ("%Y-%m-%d:%H:%M:%S")
                    node.setText (2, s)

                    m = hashlib.md5 ()
                    f = open (path, "rb")
                    while True :
                        d = f.read (32*1024)
                        if not d :
                           break
                        m.update (d)
                    crc = m.hexdigest ()
                    node.setText (3, crc)

                    node.size = size
                    node.time = t
                    node.crc = crc
                except :
                   pass

app = QApplication (sys.argv)
win = Window ()
win.show ()
app.exec_()
