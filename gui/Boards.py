# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

import app.hardware 

from gui.icons import Ico 
from gui.icons import Icon 

class BoardsDialog(QtGui.QDialog):

	def __init__(self, parent, main):
		QtGui.QDialog.__init__(self, parent)
		self.main = main

		self.setWindowTitle("Boards")
		self.setWindowIcon(Icon(Ico.Boards))


		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setContentsMargins(0,0,0,0)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)

		headerLabel   = QtGui.QLabel("Boards")
		headerLabel.setStyleSheet("background-color: black; color: white; font-size: 20pt;")

		mainLayout.addWidget(headerLabel)

		#######################################
		## Tree
		#######################################
		self.tree = QtGui.QTreeWidget()
		mainLayout.addWidget(self.tree)
		
		self.tree.setRootIsDecorated(True)
		self.tree.setAlternatingRowColors(False)
		self.tree.headerItem().setText(0, "#")
		self.connect(self.tree, QtCore.SIGNAL("itemDoubleClicked (QTreeWidgetItem *,int)"), self.on_tree_double_clicked)
		self.connect(self.tree, QtCore.SIGNAL("itemClicked (QTreeWidgetItem *,int)"), self.on_tree_clicked)

		self.load_file()

	def load_file(self):
		print "foo"
		boards = app.hardware.Boards(self.main)
		print boards.index()


	def on_tree_clicked(self, item, col):
		pass

	def on_tree_double_clicked(self, item, col):
		pass
		