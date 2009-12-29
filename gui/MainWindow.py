# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

import app.settings
import app.util
import app.Boards

import gui.FileSystemBrowser

from gui.SettingsDialog import SettingsDialog
from gui.WebSitesDialog import WebSitesDialog

from gui.HelpWidgets import HelpDockWidget
from gui.APIBrowser import APIBrowser
from gui.Browser import Browser

from gui.BoardsDialog import BoardsDialog
from gui.BootLoadersDialog import BootLoadersDialog


from gui.SketchListWidgets import SketchesBrowser
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

		
		self.setWindowTitle("Arduino-pyqt - alpha lily daffodil version | no flashing lights as yet")
		self.setWindowIcon(Icon(Ico.Arduino))
		self.setMinimumWidth(1200)
		self.setMinimumHeight(900)

		self.setDockNestingEnabled(True)
		self.setDockOptions(QtGui.QMainWindow.ForceTabbedDocks | QtGui.QMainWindow.VerticalTabs)

		self.topToolBar = QtGui.QToolBar()
		self.topToolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		self.addToolBar( self.topToolBar )
		#if self.DEV:
			#self.topToolBar.addAction("Load Keywords", self.on_dev_load_keywords)

		##############################################################
		## Files Menu
		##############################################################
		menuFiles 	= self.menuBar().addMenu( "Files" )
		menuSettings = menuFiles.addAction(Icon(Ico.Settings), "Settings", self.on_settings_dialog)
		#self.topToolBar.addAction(menuSettings)


		##############################################################
		## View Menu
		##############################################################
		menuView = self.menuBar().addMenu( "View")
		self.groupViewActions = QtGui.QActionGroup(self)
		self.connect(self.groupViewActions, QtCore.SIGNAL("triggered (QAction *)"), self.on_action_view)

		views = []
		views.append(['sketches', Ico.Sketches, "Sketches"])
		views.append(['api_browser', Ico.Function, "API Browser"])
		views.append(['help', Ico.Help, "Help"])
		views.append(['file_system_borwser', Ico.FileSystemBrowser, "Files Browser"])

		for ki, ico, caption in views:
			act = menuView.addAction(Icon(ico), caption)
			act.setProperty("ki", ki)
			self.topToolBar.addAction(act)
			self.groupViewActions.addAction(act)
		self.topToolBar.addSeparator()

		##############################################################
		## Sketch Menu
		##############################################################

		menuSketch  = self.menuBar().addMenu( "Sketches" )


		
		
		

		##############################################################
		## Hardware Menu
		##############################################################
		menuHardware 	= self.menuBar().addMenu( "Hardware" )

		## Boards
		self.actionGroupBoards = QtGui.QActionGroup(self)
		self.actionGroupBoards.setExclusive(True)
		self.connect(self.actionGroupBoards, QtCore.SIGNAL("triggered(QAction *)"), self.on_action_select_board)
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
		self.topToolBar.addSeparator()

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
		

		#self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, userSketchesWidget)	
		#self.connect(userSketchesWidget, QtCore.SIGNAL("open_sketch"), self.on_open_sketch)
		"""
		exampleSketchesWidget = SketchListWidget("Examples", self, self)
		self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, exampleSketchesWidget)	
		self.connect(exampleSketchesWidget, QtCore.SIGNAL("open_sketch"), self.on_open_sketch)
		self.tabifyDockWidget(userSketchesWidget, exampleSketchesWidget)
		"""
		helpDockWidget = HelpDockWidget("Help", self, self)
		self.addDockWidget(QtCore.Qt.RightDockWidgetArea, helpDockWidget)
		
		##########################################################
		## Central Widget
		##########################################################

		self.mainTabWidget = QtGui.QTabWidget(self)
		self.mainTabWidget.setTabsClosable(True)
		self.mainTabWidget.setMovable(True)
		self.setCentralWidget(self.mainTabWidget)
		self.connect(self.mainTabWidget, QtCore.SIGNAL("tabCloseRequested (int)"), self.on_close_tab_requested)


		self.on_action_view(QtCore.QString("sketches"))
		self.on_action_view(QtCore.QString("welcome"))

		
		edit = EditorWidget(self, self, arduino_mode=True)
		idx = self.mainTabWidget.addTab(edit, Icon(Ico.Sketch), "Foo Bar")
		self.mainTabWidget.setCurrentIndex(idx)
		edit.load_file("/home/arduino/sketchbook/chicken_shit/chicken_shit.pde", idx)

		

		#self.addDockWidget(QtCore.Qt.RightDockWidgetArea, apiBrowser)

		##########################################################
		## Status Bar
		##########################################################
		self.statusBar().addPermanentWidget(QtGui.QLabel("Board:"))
		self.lblBoard = QtGui.QLabel("-- none --")
		self.statusBar().addPermanentWidget(self.lblBoard)

		self.statusBar().addPermanentWidget(QtGui.QLabel("Bootloader:"))
		self.lblBootloader = QtGui.QLabel("-- none --")
		self.statusBar().addPermanentWidget(self.lblBootloader)

		##########################################################
		## Globally Shared Widgets
		##########################################################
		self.boards = app.Boards.Boards(self)
		self.connect(self.boards, QtCore.SIGNAL("board_selected"), self.on_board_selected)
		self.boards.load_current() ## THIS actually sets current as event above is not fired in constructor

		#self.api = app.API.API(self)
		self.on_refresh_settings()


	#########################################
	## View  Actions
	def on_action_view(self, strOrObject):
		if isinstance(strOrObject, QtCore.QString):
			ki = strOrObject
		else:
			ki = strOrObject.property("ki").toString()
		idx = None

		if ki == 'api_browser':
			apiBrowser = APIBrowser(self, self)
			idx = self.mainTabWidget.addTab(apiBrowser, Icon(Ico.Function), "API Browser")


		elif ki == "file_system_borwser":
			fileSystemBrowser = gui.FileSystemBrowser.FileSystemBrowser(self, self)
			idx = self.mainTabWidget.addTab(fileSystemBrowser, Icon(Ico.FileSystemBrowser), "Files Browser")

		elif ki == 'sketches':
			sketchesWidget = SketchesBrowser( self, self )
			idx = self.mainTabWidget.addTab(sketchesWidget, Icon(Ico.Sketches), "Sketches")
			self.connect(sketchesWidget, QtCore.SIGNAL("open_sketch"), self.on_open_sketch)

		elif ki == 'welcome':
			welcomePage = Browser(self, self, "welcome.html")
			self.mainTabWidget.addTab(welcomePage, Icon(Ico.Arduino), "Welcome")

		if idx:
			self.mainTabWidget.setCurrentIndex(idx)

	#########################################
	## Board Stuff
	def on_action_boards(self):
		d = BoardsDialog(self, self)
		d.show()

	def on_action_select_board(self, act):
		self.boards.set_current(act.property("board").toString())

	def on_board_selected(self, board):
		self.lblBoard.setText(board['name'])
		self.menuBoards.setTitle(board['name'])

	#########################################
	## Bootloader Stuff
	def on_action_bootloaders(self):
		d = BootLoadersDialog(self, self)
		d.show()

	def on_action_bootloader_burn(self, act):
		self.lblBootloader.setText(act.text())


	#########################################
	## Tab Events
	def on_close_tab_requested(self, tabIndex):
		self.mainTabWidget.removeTab(tabIndex)

	#########################################
	## Open Sketchboox
	def on_open_sketch(self, file_path):
		print "OPEN", file_path
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
		current = self.boards.current()
		if current:
			current = current['name']
		for board, caption in self.boards.index():
			act = self.menuBoards.addAction( caption )
			act.setProperty("board", board )
			act.setCheckable(True)
			if board == current:
				act.setChecked(True)
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