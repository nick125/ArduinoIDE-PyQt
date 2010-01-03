# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from gui.widgets import GenericWidgets

from gui.icons import Ico 
from gui.icons import Icon 

from app.settings import settings

"""
Displays the directories for sketches
Currently two modes, broswse USER sketches, or Examples

TODO - maybe these need to be split up and have more than one directory sets
"""

########################################################################
## Sketches Browser - sketches and examples in 2 cols in central widget
########################################################################
class SketchesBrowser(QtGui.QSplitter):
	def __init__(self,  parent, main):
		QtGui.QDockWidget.__init__(self, parent)

		self.main = main

		sketchesWidget = SketchListWidget("Sketches", self, self.main)
		self.addWidget(sketchesWidget)
		self.connect(sketchesWidget, QtCore.SIGNAL("open_sketch"), self.on_open_sketch)

		examplesWidget = SketchListWidget("Examples", self, self.main)
		self.addWidget(examplesWidget)
		self.connect(examplesWidget, QtCore.SIGNAL("open_sketch"), self.on_open_sketch)
		
	def on_open_sketch(self, file_path):
		self.emit(QtCore.SIGNAL("open_sketch"), file_path)

#################################################################
## UNUSED DockWidget
class UNUSED_SketchListDockWidget(QtGui.QDockWidget):

	MODE_USER = 0
	MODE_EXAMPES = 1
	
	def __init__(self, title, parent, main):
		QtGui.QDockWidget.__init__(self, title, parent)

		self.main = main
		
		containerWidget = QtGui.QWidget()
		self.setWidget(containerWidget)

		self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)

#################################################################
## Sketches Tree/widgets - browses a directory - "ki" is set on title = "Examples" == dodgy
#################################################################
class SketchListWidget(QtGui.QWidget):
	
	def __init__(self, title, parent, main):
		QtGui.QWidget.__init__(self, parent)

		self.main = main
		if title == "Examples": ## TODO sody path to view
			self.dir_to_browse = settings.examples_path()
		else:
			self.dir_to_browse = settings.sketches_path()

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setContentsMargins(0, 0, 0, 0)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)

		headLabel = GenericWidgets.HeaderLabel(self, self.main, icon=Ico.Sketches, title=title, color="black", wash_to="#456D91")
		mainLayout.addWidget(headLabel)

		self.statusWidget = GenericWidgets.StatusWidget(self)

		## redundant listings tree of bookmaarks.. maybe later
		if 1 == 0:
			self.treePlaces = QtGui.QTreeWidget()
			mainLayout.addWidget(self.treePlaces, 1)
			self.treePlaces.headerItem().setText(0, "Location")
			self.treePlaces.headerItem().setText(1, "Path")
			self.treePlaces.header().hide()
			self.treePlaces.setColumnHidden(1, True)
			self.treePlaces.setRootIsDecorated(False)
			self.treePlaces.setAlternatingRowColors(True)
			self.connect(self.treePlaces, QtCore.SIGNAL("itemClicked (QTreeWidgetItem *,int)"), self.on_tree_place_clicked)
			for panel in [["Examples", settings.examples_path()], ["Sketches", settings.sketchbooks_path()]]:
				item = QtGui.QTreeWidgetItem()
				self.treePlaces.addTopLevelItem(item)
				item.setText(0, panel[0])
				font = item.font(0)
				font.setBold(True)
				item.setFont(0, font)
				item.setIcon(0, Icon(Ico.Folder))
				if panel[1]:
					item.setText(1, panel[1])

			self.dir_to_browse = None


		toolbar = QtGui.QToolBar(self)
		toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		mainLayout.addWidget( toolbar )
		
		self.toolButtonGroup = QtGui.QButtonGroup(self)
		self.toolButtonGroup.setExclusive(True)
		self.connect(self.toolButtonGroup, QtCore.SIGNAL("buttonClicked(QAbstractButton *)"), self.on_view_selected)

		listButton = QtGui.QToolButton()
		listButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		listButton.setText("Tree")
		listButton.setIcon(Icon(Ico.Black))
		listButton.setStyleSheet("padding: 0px; margin: 0px;")
		listButton.setCheckable(True)
		listButton.setChecked(True)
		toolbar.addWidget(listButton)
		self.toolButtonGroup.addButton(listButton, 0)

		listButton = QtGui.QToolButton()
		listButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		listButton.setText("List")
		listButton.setIcon(Icon(Ico.Yellow))
		listButton.setStyleSheet("padding: 0px; margin: 0px;")
		listButton.setCheckable(True)
		toolbar.addWidget(listButton)
		self.toolButtonGroup.addButton(listButton, 1)

		#######################################
		## Tree
		#######################################
		self.tree = QtGui.QTreeWidget()
		mainLayout.addWidget(self.tree, 10)
		
		self.tree.setSortingEnabled(True)
		self.tree.setRootIsDecorated(True)
		self.tree.setAlternatingRowColors(False)
		self.tree.headerItem().setText(0, "Files")
		self.connect(self.tree, QtCore.SIGNAL("itemDoubleClicked (QTreeWidgetItem *,int)"), self.on_tree_double_clicked)
		self.connect(self.tree, QtCore.SIGNAL("itemClicked (QTreeWidgetItem *,int)"), self.on_tree_clicked)

		self.load_list()

	def on_tree_place_clicked(self, item, col):
		self.dir_to_browse = item.text(1)
		self.load_list()
		

	def on_view_selected(self, button):
		for bitt in self.toolButtonGroup.buttons():
			if bitt.isChecked():
				bitt.setIcon(Icon(Ico.Yellow))
			else:
				bitt.setIcon(Icon(Ico.Black))
		self.load_list()

	#################################################################
	## Tree Events
	#################################################################
	def on_tree_clicked(self, item, col):
		return
		
		

	def on_tree_double_clicked(self, item, col):
		data = item.data(0, QtCore.Qt.UserRole)
		if not data.isNull():
			self.emit(QtCore.SIGNAL("open_sketch"), data.toString())


	#################################################################
	## Load List
	#################################################################
	def load_list(self):
		self.tree.model().removeRows(0, self.tree.model().rowCount())
		if not self.dir_to_browse:
			self.statusWidget.set_status(self.tree, "No directory")
			return
		if not self.dir_to_browse.exists('.'):
			QtGui.QMessageBox.information(self, "Error", "The directory %s was not found" % self.dir_to_browse.absolutePath())
			return
		self.walk_dir(self.dir_to_browse,  self.tree.invisibleRootItem())
		self.tree.sortItems(0, QtCore.Qt.AscendingOrder)

	def walk_dir(self, dir_path, parentNode):
		## Grab the children of the path
		files = dir_path.entryInfoList(QtCore.QDir.AllEntries | QtCore.QDir.NoDotAndDotDot)
		## The mode of the tree. 
		isList = (self.toolButtonGroup.checkedId() == 1)
		## Recurse through the files
		for child in files:
			if child.isDir():
				# Add the child directory and scan it
				if isList:
					self.walk_dir(QtCore.QDir(child.absoluteFilePath()), parentNode)
				else:
					treeItem = QtGui.QTreeWidgetItem(parentNode)
					treeItem.setText(0, child.fileName())
					treeItem.setIcon(0, Icon(Ico.Folder))
					self.walk_dir(QtCore.QDir(child.absoluteFilePath()), treeItem)
					
			else:
				# Add it as a file
				if child.suffix() == 'pde':
					treeItem = QtGui.QTreeWidgetItem(parentNode)
					treeItem.setText(0, child.fileName()) 
					treeItem.setData(0, QtCore.Qt.UserRole, child.filePath())
					treeItem.setIcon(0, Icon(Ico.Sketch))
