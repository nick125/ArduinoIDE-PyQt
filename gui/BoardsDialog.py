# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.Qsci import QsciScintilla

from gui.widgets.EditorWidget import EditorWidget
from gui.icons import Ico 
from gui.icons import Icon 

class BoardsDialog(QtGui.QDialog):
	"""
		A dialog to display the different Arduino boards
	"""

	def __init__(self, parent, main):
		QtGui.QDialog.__init__(self, parent)
		self.main = main

		self.setWindowTitle("Boards")
		self.setWindowIcon(Icon(Ico.Boards))
		self.setMinimumWidth(700)
		self.setMinimumHeight(500)

		mainLayout = QtGui.QVBoxLayout()
		m = 0
		mainLayout.setContentsMargins(m, 10, m, m)
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


		self.editor = EditorWidget(self, self.main, arduino_mode=False)
		tabWidget.addTab(self.editor, "boards.txt")
		

		self.statusBar = QtGui.QStatusBar()
		mainLayout.addWidget(self.statusBar)

		self.load_file()

	def load_file(self):
		self.editor.load_file(self.main.settings.hardware_path("boards.txt"))
		
		## Loop the boards
		boards = self.main.boards.all()
		for board in boards:
			boardItem = QtGui.QTreeWidgetItem()
			self.tree.addTopLevelItem(boardItem)
			boardItem.setIcon(0, Icon(Ico.Board))
			boardItem.setText(0, boards[board]['name'])
			font = boardItem.font(0)
			font.setBold(True)
			boardItem.setFont(0, font)
			boardItem.setFirstColumnSpanned(True)

			## loop each section andn ignore 'name'
			for section in boards[board]:
				if section == 'name':
					pass
				else:
					sectionItem = QtGui.QTreeWidgetItem(boardItem)
					sectionItem.setText(0, section)
					sectionItem.setFirstColumnSpanned(True)

					## loops dic properties
					if isinstance(boards[board][section], dict):
						for prop in boards[board][section]:
							propItem = QtGui.QTreeWidgetItem(sectionItem)
							propItem.setText(1, prop)					
							propItem.setText(2, boards[board][section][prop])	
							
					
		for i in range(1, 3):
			self.tree.resizeColumnToContents(i)
		self.tree.sortByColumn(0, QtCore.Qt.AscendingOrder)
		self.statusBar.showMessage("%s boards" % self.tree.invisibleRootItem().childCount() )

	def on_tree_clicked(self, item, col):
		pass

	def on_tree_double_clicked(self, item, col):
		pass
		
