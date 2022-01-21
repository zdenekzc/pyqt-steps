import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *

class DbView (QMainWindow):

   def __init__ (self, parent = None) :
       super (DbView, self).__init__ (parent)

       tree = QTreeWidget (self)
       table = QTableView (self)

       splitter = QSplitter (self)
       splitter.setOrientation (Qt.Horizontal)
       splitter.addWidget (tree)
       splitter.addWidget (table)

       self.setCentralWidget (splitter)

       db = QSqlDatabase.addDatabase ("QSQLITE")
       # db.setDatabaseName (":memory:")
       db.setDatabaseName ("test.sqlite")
       db.open ()

       query = db.exec_ ("CREATE TABLE IF NOT EXISTS colors (name TEXT PRIMARY KEY, red INTEGER, green INTEGER, blue INTEGER)")

       db.exec_ ("INSERT INTO colors (name, red, green, blue) VALUES (\"blue\", 0, 0, 255)")

       insert = QSqlQuery (db)
       insert.prepare ("INSERT INTO colors (name, red, green, blue) VALUES (:name, :red, :green, :blue)")
       insert.bindValue (":name", "green")
       insert.bindValue (":red", QVariant (0))
       insert.bindValue (":green", QVariant (255))
       insert.bindValue (":blue", QVariant (0))
       insert.exec_ ()

       model = QSqlTableModel (self, db)
       model.setTable ("colors")
       model.select ()

       table.setModel (model)

       database_node = QTreeWidgetItem (tree)
       database_node.setText (0, db.databaseName())
       database_node.setForeground (0, QColor ("lime"))

       table_list = db.tables()
       for table_name in table_list :
           query = db.exec_ ("SELECT * FROM " + table_name)

           table_node = QTreeWidgetItem (database_node)
           table_node.setText (0, table_name)
           table_node.setForeground  (0, QColor ("orange"))

           rec = query.record ()
           for k in range (rec.count ()) :
              txt = rec.fieldName (k)
              column_node = QTreeWidgetItem (table_node)
              column_node.setText (0, txt)
              column_node.setForeground  (0, QColor ("blue"))

       tree.expandAll ()

if __name__ == "__main__" :
   app = QApplication (sys.argv)
   win = DbView ()
   win.show ()
   app.exec_ ()
