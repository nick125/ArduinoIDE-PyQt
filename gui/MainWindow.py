# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

import app.settings
import app.util
import app.hardware

from gui.HeaderWidget import HeaderWidget
from gui.Browser import Browser

from gui.HelpWidget import HelpWidget
from gui.SketchListWidget import SketchListWidget
from gui.EditorWidget import EditorWidget

from gui.icons import Ico 
from gui.icons import Icon 

class MainWindow(QtGui.QMainWindow):


	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self)

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
		##########################################################
		## Main Menus
		##########################################################
		menuFiles 	= self.menuBar().addMenu( "Files" )
		menuEdit 	= self.menuBar().addMenu( "Edit" )
		menuSketch  = self.menuBar().addMenu( "Sketch" )
		menuTools 	= self.menuBar().addMenu( "Tools" )
		menuHelp 	= self.menuBar().addMenu( "Help" )


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

		## Welcome page
		welcomePage = Browser(self, self, "welcome.html")
		self.mainTabWidget.addTab(welcomePage, Icon(Ico.Arduino), "Welcome")


		##########################################################
		## Right Dock
		##########################################################
		helpWidget = HelpWidget(self)
		self.addDockWidget(QtCore.Qt.RightDockWidgetArea, helpWidget)


		self.load_programmers()


	def load_programmers(self):
		programmers = app.hardware.Programmers(self)
		


	def on_open_sketch(self, file_path, file_contents):
		fileInfo = QtCore.QFileInfo(file_path)
		newEditor = EditorWidget(self)
		newEditor.set_source(file_contents)
		newTab = self.mainTabWidget.addTab(newEditor, Icon(Ico.Sketch), fileInfo.fileName())
		self.mainTabWidget.setCurrentIndex(newTab)