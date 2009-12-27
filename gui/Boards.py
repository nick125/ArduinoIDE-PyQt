# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

import app.hardware 

import gui.widgets
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

		#headerLabel   = gui,widgets.HeaderLabel(self, self.main, title="Boards
		#headerLabel.setStyleSheet("background-color: black; color: white; font-size: 20pt;")

		#mainLayout.addWidget(headerLabel)

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
		for i in boards.tree():
			print foo;


	def on_tree_clicked(self, item, col):
		pass

	def on_tree_double_clicked(self, item, col):
		pass
		