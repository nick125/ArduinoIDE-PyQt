# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

import app.settings
import app.util
import app.Boards
import app.Bootloaders
import app.Parsers

from gui.SettingsDialog import SettingsDialog
from gui.WebSitesDialog import WebSitesDialog

from gui.HelpWidgets import HelpDockWidget
from gui.Browser import Browser

from gui.BoardsDialog import BoardsDialog
from gui.BootLoadersDialog import BootLoadersDialog


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
		self.parsers = app.Parsers.Parsers()
		
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

		##############################################################
		## Files Menu
		##############################################################
		menuFiles 	= self.menuBar().addMenu( "Files" )
		menuSettings = menuFiles.addAction(Icon(Ico.Settings), "Settings", self.on_settings_dialog)
		self.topToolBar.addAction(menuSettings)

		#menuEdit 	= self.menuBar().addMenu( "Edit" )

		##############################################################
		## Sketch Menu
		##############################################################

		menuSketch  = self.menuBar().addMenu( "Sketch Books" )
		
		

		##############################################################
		## Hardware Menu
		##############################################################
		menuHardware 	= self.menuBar().addMenu( "Hardware" )

		## Boards
		self.actionGroupBoards = QtGui.QActionGroup(self)
		self.actionGroupBoards.setExclusive(True)
		self.connect(self.actionGroupBoards, QtCore.SIGNAL("triggered(QAction *)"), self.on_action_board_select)
		self.menuBoards = menuHardware.addMenu(Icon(Ico.Board), "-- No Board Selected --") # populates later
		act = menuHardware.addAction(Icon(Ico.Boards), "Boards", self.on_action_boards)
		self.topToolBar.addAction(act)
		menuHardware.addSeparator()

		## Bootloaders
		self.actionGroupBootLoaders = QtGui.QActionGroup(self)
		self.actionGroupBootLoaders.setExclusive(True)
		self.connect(self.actionGroupBootLoaders, QtCore.SIGNAL("triggered(QAction *)"), self.on_action_bootloader_burn)
		self.menuBootLoaders = menuHardware.addMenu(Icon(Ico.BootLoaderBurn), "Burn Bootloader") # populates later
		act = menuHardware.addAction(Icon(Ico.BootLoaders), "Bootloaders", self.on_action_bootloaders)
		self.topToolBar.addAction(act)
		menuHardware.addSeparator()

		##############################################################
		## Websites Menu
		##############################################################
		self.menuWebSites 	= self.menuBar().addMenu("Websites" )
	
		self.menuWebSites.addSeparator()
		self.actionEditWebsites = self.menuWebSites.addAction( "Edit Sites", self.on_websites_dialog )

		##############################################################
		## Help Menu
		##############################################################
		menuHelp 	= self.menuBar().addMenu( "Help" )

		##########################################################
		## Header Label 
		##########################################################	
		#lblHeader = HeaderWidget(self)
		#self.addDockWidget(QtCore.Qt.TopDockWidgetArea, lblHeader)	
		
	
		##########################################################
		## Left Dock
		##########################################################
		userSketchesWidget = SketchListWidget(self, self)
		self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, userSketchesWidget)	
		self.connect(userSketchesWidget, QtCore.SIGNAL("open_sketch"), self.on_open_sketch)

		#userSketchesWidget2 = SketchListWidget(self, self)
		#self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, userSketchesWidget2)	
		#self.connect(userSketchesWidget2, QtCore.SIGNAL("open_sketch"), self.on_open_sketch)
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
		#apiBrowser = gui.APIBrowser.APIBrowser(self, self)
		#self.mainTabWidget.addTab(apiBrowser, Icon(Ico.Arduino), "API Browser")

		import gui.FileSystemBrowser
		fileSystemBrowser = gui.FileSystemBrowser.FileSystemBrowser(self, self)
		self.mainTabWidget.addTab(fileSystemBrowser, Icon(Ico.Folder), "Files Browser")


		## Welcome page
		#welcomePage = Browser(self, self, "welcome.html")
		#self.mainTabWidget.addTab(welcomePage, Icon(Ico.Arduino), "Welcome")


		##########################################################
		## Right Dock
		##########################################################
		#helpDockWidget = HelpDockWidget(self, self)
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

		self.on_refresh_settings()

	#########################################
	## Board Events
	def on_action_boards(self):
		print "boards"
		d = BoardsDialog(self, self)
		d.show()

	def on_action_board_select(self, act):
		print "on_action_board", act
		self.lblBoard.setText(act.text())
		self.menuBoards.setTitle(act.text())

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
		newEditor = EditorWidget(self, self, arduino_mode=True)
		newEditor.load_file(fileInfo.filePath())
		newTab = self.mainTabWidget.addTab(newEditor, Icon(Ico.Sketch), fileInfo.fileName())
		self.mainTabWidget.setCurrentIndex(newTab)


	def on_dev_load_keywords(self):
		import app.keywords
		
		keyw = app.keywords.Keywords(self)
		print keyw.index()


	def on_settings_dialog(self):
		d = SettingsDialog(self, self)
		self.connect(d, QtCore.SIGNAL("refresh_settings"), self.on_refresh_settings)
		if d.exec_():
			self.on_refresh_settings()

	def on_refresh_settings(self):
		
		## Load Boards Menu
		for act in self.actionGroupBoards.actions():
			self.actionGroupBoards.removeAction(act)
		file_path = self.settings.hardware_path("boards.txt")
		if file_path:
			dic = self.ut.load_arduino_config_file(file_path)
			for ki in dic:
				act = self.menuBoards.addAction( dic[ki]['name'] )
				act.setCheckable(True)
				self.actionGroupBoards.addAction(act)

		## Laod bootloaders
		for act in self.actionGroupBootLoaders.actions():
			self.actionGroupBootLoaders.removeAction(act)
		file_path = self.settings.hardware_path("programmer.txt")
		if file_path:
			dic = self.ut.load_arduino_config_file(file_path)
			for ki in dic:
				print ki
				act = self.menuBootLoaders.addAction( ki )
				act.setCheckable(True)
				self.actionGroupBootLoaders.addAction(act)

			

	def on_websites_dialog(self):
		d = WebSitesDialog(self, self)
		d.show()