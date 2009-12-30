# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.Qsci import QsciScintilla

from gui.icons import Ico 
from gui.icons import Icon 

from gui.widgets.EditorWidget import EditorWidget

class BootLoadersDialog(QtGui.QDialog):

	def __init__(self, parent, main):
		QtGui.QDialog.__init__(self, parent)
		self.main = main

		self.setWindowTitle("Boot Loaders")
		self.setWindowIcon(Icon(Ico.BootLoaders))
		self.setMinimumWidth(500)
		self.setMinimumHeight(400)

		mainLayout = QtGui.QVBoxLayout()
		m = 0
		mainLayout.setContentsMargins(m,10,m,m)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)

		tabWidget = QtGui.QTabWidget()
		mainLayout.addWidget(tabWidget)

		#######################################
		## Tree Tab
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

		#######################################
		## Editor Tab	
		self.editor = EditorWidget(self, self.main)
		tabWidget.addTab(self.editor, "programmers.txt")


		#######################################
		## Status Bar	
		self.statusBar = QtGui.QStatusBar()
		mainLayout.addWidget(self.statusBar)

		self.load_file()


	def load_file(self):

		file_path = self.main.settings.hardware_path().absoluteFilePath("programmers.txt")
		#source = self.main.ut.get_file_contents(file_path)
		self.editor.load_file(file_path)
		boot_loaders = self.main.ut.load_arduino_config_file(file_path)

		c = 0
		for boot_loader in boot_loaders:
			c += 1
			bootLoaderItem = QtGui.QTreeWidgetItem()
			self.tree.addTopLevelItem(bootLoaderItem)
			bootLoaderItem.setIcon(0, Icon(Ico.BootLoader))
			bootLoaderItem.setText(0, boot_loaders[boot_loader]['name'])
			font = bootLoaderItem.font(0)
			font.setBold(True)
			bootLoaderItem.setFont(0, font)
			bootLoaderItem.setFirstColumnSpanned(True)

			del boot_loaders[boot_loader]['name'] # nuke "name" node used above
			for prop in boot_loaders[boot_loader]:
				propItem = QtGui.QTreeWidgetItem(bootLoaderItem)
				propItem.setText(1, prop)
				propItem.setText(2, boot_loaders[boot_loader][prop])	
			
							
		for i in range(2, 3):
			self.tree.resizeColumnToContents(i)
		self.tree.sortByColumn(0, QtCore.Qt.AscendingOrder)
		self.statusBar.showMessage("%s items" % c)

	def on_tree_clicked(self, item, col):
		pass

	def on_tree_double_clicked(self, item, col):
		pass
		
