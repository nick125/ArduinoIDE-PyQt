# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

import app.settings
import app.util
import app.Boards
import app.Bootloaders

from gui.HelpWidgets import HelpDockWidget
from gui.Browser import Browser

from gui.Boards import BoardsDialog
from gui.Bootloaders import BootloadersDialog


from gui.SketchListWidget import SketchListWidget
from gui.EditorWidget import EditorWidget

from gui.icons import Ico 
from gui.icons import Icon 

class MainWindow(QtGui.QMainWindow):


	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self)
		self.DEV = True

		# TODO - User customisable style
		QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))

		## Sets up the settings and other global classes
		self.settings = app.settings.Settings() 
		self.ut = app.util.Util()
		
		self.setWindowTitle("Arduino - pyqt - alpha version")
		self.setWindowIcon(Icon(Ico.Arduino))
		self.setMinimumWidth(1200)
		self.setMinimumHeight(900)
		self.setDockNestingEnabled(True)
		self.setDockOptions(QtGui.QMainWindow.ForceTabbedDocks)

		self.topToolBar = QtGui.QToolBar()
		self.topToolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		self.addToolBar( self.topToolBar )
		if self.DEV:
			self.topToolBar.addAction("Load Keywords", self.on_dev_load_keywords)

		##########################################################
		## Main Menus
		##########################################################
		menuFiles 	= self.menuBar().addMenu( "Files" )
		menuEdit 	= self.menuBar().addMenu( "Edit" )
		menuSketch  = self.menuBar().addMenu( "Sketch" )
		
		menuHelp 	= self.menuBar().addMenu( "Help" )

		##############################################################
		## Tools Menu
		##############################################################
		menuTools 	= self.menuBar().addMenu( "Tools" )

		## Boards
		self.actionGroupBoards = QtGui.QActionGroup(self)
		self.actionGroupBoards.setExclusive(True)
		self.connect(self.actionGroupBoards, QtCore.SIGNAL("triggered(QAction *)"), self.on_action_board_select)
		self.menuBoards = menuTools.addMenu(Icon(Ico.Board), "Select Board")
		boards = app.Boards.Boards(self)
		for b in boards.index():
			act = self.menuBoards.addAction( b )
			act.setCheckable(True)
			self.actionGroupBoards.addAction(act)
		act = menuTools.addAction(Icon(Ico.Boards), "Boards Overview", self.on_action_boards)
		self.topToolBar.addAction(act)
		menuTools.addSeparator()

		## Bootloaders
		self.actionGroupBootLoaders = QtGui.QActionGroup(self)
		self.actionGroupBootLoaders.setExclusive(True)
		self.connect(self.actionGroupBootLoaders, QtCore.SIGNAL("triggered(QAction *)"), self.on_action_bootloader_burn)
		self.menuBootLoaders = menuTools.addMenu(Icon(Ico.BootloaderBurn), "Burn Bootloader")
		programmers = app.Boards.Programmers(self)
		for p in programmers.index():
			act = self.menuBootLoaders.addAction( p )
			act.setCheckable(True)
			self.actionGroupBootLoaders.addAction(act)
		act = menuTools.addAction(Icon(Ico.Bootloaders), "Bootloaders Overview", self.on_action_bootloaders)
		self.topToolBar.addAction(act)
		menuTools.addSeparator()

		##########################################################
		## Header Label 
		##########################################################	
		#lblHeader = HeaderWidget(self)
		#self.addDockWidget(QtCore.Qt.TopDockWidgetArea, lblHeader)	
		
	
		##########################################################
		## Left Dock
		##########################################################
		userSketchesWidget = SketchListWidget(self, SketchListWidget.MODE_USER)
		self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, userSketchesWidget)	
		self.connect(userSketchesWidget, QtCore.SIGNAL("open_sketch"), self.on_open_sketch)
		#exampleSketchesWidget = SketchListWidget(self, SketchListWidget.MODE_EXAMPES)
		#self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, exampleSketchesWidget)	



		##########################################################
		## Central Widget
		##########################################################
		self.mainTabWidget = QtGui.QTabWidget(self)
		self.mainTabWidget.setTabsClosable(True)
		self.setCentralWidget(self.mainTabWidget)

		#import gui.DefEditor
		#defEditor = gui.DefEditor.DefEditor(self, self)
		#self.mainTabWidget.addTab(defEditor, Icon(Ico.Arduino), "Def Editor")
		import gui.APIBrowser
		apiBrowser = gui.APIBrowser.APIBrowser(self, self)
		#self.mainTabWidget.addTab(apiBrowser, Icon(Ico.Arduino), "API Browser")

		import gui.FileSystemBrowser
		fileSystemBrowser = gui.FileSystemBrowser.FileSystemBrowser(self, self)
		self.mainTabWidget.addTab(fileSystemBrowser, Icon(Ico.Folder), "Files Browser")


		## Welcome page
		welcomePage = Browser(self, self, "welcome.html")
		self.mainTabWidget.addTab(welcomePage, Icon(Ico.Arduino), "Welcome")


		##########################################################
		## Right Dock
		##########################################################
		helpDockWidget = HelpDockWidget(self, self)
		#self.addDockWidget(QtCore.Qt.RightDockWidgetArea, helpDockWidget)

		##########################################################
		## Status Bar
		##########################################################
		self.statusBar().addPermanentWidget(QtGui.QLabel("Board:"))
		self.lblBoard = QtGui.QLabel("-- none --")
		self.statusBar().addPermanentWidget(self.lblBoard)

		self.statusBar().addPermanentWidget(QtGui.QLabel("Bootloader:"))
		self.lblBootloader = QtGui.QLabel("-- none --")
		self.statusBar().addPermanentWidget(self.lblBootloader)

		

	#########################################
	## Board Stuff
	def on_action_boards(self):
		print "boards"
		d = BoardsDialog(self, self)
		d.show()

	def on_action_board_select(self, act):
		print "on_action_board", act
		self.lblBoard.setText(act.text())

	#########################################
	## Bootloader Stuff
	def on_action_bootloaders(self):
		d = BootLoadersDialog(self, self)
		d.show()

	def on_action_bootloader_burn(self, act):
		print "on_action_bootloader_burn", act
		self.lblBootloader.setText(act.text())



	def on_open_sketch(self, file_path):
		fileInfo = QtCore.QFileInfo(file_path)
		newEditor = EditorWidget(self)
		newEditor.open_file(fileInfo.filePath())
		newTab = self.mainTabWidget.addTab(newEditor, Icon(Ico.Sketch), fileInfo.fileName())
		self.mainTabWidget.setCurrentIndex(newTab)


	def on_dev_load_keywords(self):
		import app.keywords
		
		keyw = app.keywords.Keywords(self)
		print keyw.index()
"""
class StatusWidget(QtCore.QWidget):

		def __init__(self, parent, label="label", value="value",):
			QtCore.QWidget.__init__(self, parent)
"""
		