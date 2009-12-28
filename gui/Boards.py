# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.Qsci import QsciScintilla
#import app.Boards 

import gui.widgets
from gui.icons import Ico 
from gui.icons import Icon 

class BoardsDialog(QtGui.QDialog):

	def __init__(self, parent, main):
		QtGui.QDialog.__init__(self, parent)
		self.main = main

		self.setWindowTitle("Boards")
		self.setWindowIcon(Icon(Ico.Boards))
		self.setMinimumWidth(700)
		self.setMinimumHeight(500)

		mainLayout = QtGui.QVBoxLayout()
		m = 0
		mainLayout.setContentsMargins(m,10,m,m)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)

		tabWidget = QtGui.QTabWidget()
		mainLayout.addWidget(tabWidget)

		#######################################
		## Tree
		#######################################
		self.tree = QtGui.QTreeWidget()
		tabWidget.addTab(self.tree, "Tree View")
		self.connect(self.tree, QtCore.SIGNAL("itemDoubleClicked (QTreeWidgetItem *,int)"), self.on_tree_double_clicked)
		self.connect(self.tree, QtCore.SIGNAL("itemClicked (QTreeWidgetItem *,int)"), self.on_tree_clicked)

		self.tree.setAnimated(True)
		self.tree.setRootIsDecorated(True)
		self.tree.setAlternatingRowColors(False)
		self.tree.header().setStretchLastSection(True)
		self.tree.headerItem().setText(0, "")
		self.tree.headerItem().setText(1, "Property")
		self.tree.headerItem().setText(2, "Value")
		self.tree.setColumnWidth(0, 100)
		self.tree.setColumnWidth(1, 150)


		self.editor = QsciScintilla(self)
		self.editor.setUtf8(True)
		self.editor.setFolding(QsciScintilla.BoxedTreeFoldStyle)
		self.editor.setMarginLineNumbers(1, True)
		self.editor.setAutoIndent(True)
		tabWidget.addTab(self.editor, "boards.txt")
		file_path = self.main.settings.hardware_path().append("boards.txt")
		self.editor.setText(self.main.ut.get_file_contents(file_path))

		self.statusBar = QtGui.QStatusBar()
		mainLayout.addWidget(self.statusBar)

		self.load_file()

	def load_file(self):
		#print "foo"
		#boardsObj = app.Boards.Boards(self.main)
		board_file = self.main.settings.hardware_path().append("boards.txt")
		boards = self.main.ut.load_arduino_config_file(board_file)
		#print boards
		## Loop the boards
		c = 0
		for board in boards:
			c += 1
			boardItem = QtGui.QTreeWidgetItem()
			self.tree.addTopLevelItem(boardItem)
			#self.tree.setItemExpanded(boardItem, True)
			boardItem.setIcon(0, Icon(Ico.Board))
			boardItem.setText(0, boards[board]['name'])
			font = boardItem.font(0)
			font.setBold(True)
			boardItem.setFont(0, font)
			boardItem.setFirstColumnSpanned(True)
			#boardItem.setBackgroundColor(0, QtGui.QColor.fromRgb(139, 171, 203))
			## load properties section
			del boards[board]['name'] # nuke "name" node used above
			for section in boards[board]:
				sectionItem = QtGui.QTreeWidgetItem(boardItem)
				sectionItem.setText(0, section)
				sectionItem.setFirstColumnSpanned(True)
				#sectionItem.setText(1, section)
				#self.tree.setItemExpanded(sectionItem, True)

				## loops dic properties
				if isinstance(boards[board][section], dict):
					for prop in boards[board][section]:
						print "prop=", prop, boards[board][section][prop]
						
						propItem = QtGui.QTreeWidgetItem(sectionItem)
						propItem.setText(1, prop)					
						propItem.setText(2, boards[board][section][prop])	
						
					
		for i in range(1, 3):
			self.tree.resizeColumnToContents(i)
		self.tree.sortByColumn(0, QtCore.Qt.AscendingOrder)
		self.statusBar.showMessage("%s boards" % c)

	def on_tree_clicked(self, item, col):
		pass

	def on_tree_double_clicked(self, item, col):
		pass
		