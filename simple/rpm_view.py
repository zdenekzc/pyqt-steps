#!/usr/bin/env python

import sys

import dnf

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# --------------------------------------------------------------------------

class TreeItem (QTreeWidgetItem):
   pass

class RpmView (QTreeWidget):

   def __init__ (self, parent = None) :
       super (RpmView, self).__init__ (parent)

       base = dnf.Base ()
       base.read_all_repos ()
       base.fill_sack ()

       branch = TreeItem (self, "Repositories")
       branch.item_icon = "class"
       branch.setupTreeItem ()
       for repo in base.repos.iter_enabled () :
           node = TreeItem (branch, repo.id)
           node.item_tooltip = str (repo.baseurl)
           node.item_icon = "function"
           node.setupTreeItem ()
           node.obj = repo

       base.read_comps ()
       branch = TreeItem (self, "Groups")
       branch.item_icon = "class"
       branch.setupTreeItem ()

       for grp in base.comps.groups :
           group_branch = TreeItem (branch, grp.name)
           group_branch.item_icon = "class"
           group_branch.item_tooltip = grp.id
           group_branch.setupTreeItem ()
           group_branch.obj = grp

           for pkg in grp.packages_iter () :
               node = TreeItem (group_branch, pkg.name)
               node.item_icon = "function"
               node.setupTreeItem ()
               node.obj = pkg

       q = base.sack.query ()
       a = q.available ()
       self.addPackages ("Available Packages", a)

       a = q.installed ()
       self.addPackages ("Installed Packages", a)

   def addPackages (self, text, a) :
       branch = TreeItem (self, text)
       branch.item_icon = "class"
       branch.setupTreeItem ()

       for pkg in a :
           node = TreeItem (branch, pkg.name + "-" + pkg.evr + "." + pkg.arch + ".rpm")
           if pkg.installed :
              node.item_icon = "function"
           else :
              node.item_icon = "variable"
           node.item_tooltip = "downloadsize=" + str (pkg.downloadsize) + ", installsize=" + str (pkg.installsize)
           node.setupTreeItem ()
           node.obj = pkg

# --------------------------------------------------------------------------

# do not use file name rpm.py for this module

# kate: indent-width 1; show-tabs true; replace-tabs true; remove-trailing-spaces all
