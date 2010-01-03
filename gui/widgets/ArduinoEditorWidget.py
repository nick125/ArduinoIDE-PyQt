# -*- coding: utf-8 -*-

"""
The Arudino Editor contains  an 
* Editor
* Terminal Viewer
* Compiler Bar
"""

## TODO move the yaml stuff write, read encode somewhere else

import os
import yaml
from yaml import Loader, Dumper
from PyQt4 import QtCore, QtGui

import app.utils

from gui.widgets import GenericWidgets
from gui.widgets.EditorWidget import EditorWidget
from gui.widgets.TerminalWidget import TerminalWidget
from gui.widgets.ArduinoCompilerBar import ArduinoCompilerBar

from gui.icons import Ico 
from gui.icons import Icon 

"""
### the current layout

=== File ===
Editor   | arduinocompiler
ternimal | ""

"""
class ArduinoEditorWidget(QtGui.QWidget):

	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self, parent)

		self.main = main

		self.project_file_path = None
		self.project_settings_file = None
		self.project_settings = None

		mainLayout = QtGui.QHBoxLayout()
		mainLayout.setContentsMargins(0, 0, 0, 0)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)

		#########################################
		## Editor/Terminal on left, Compiler Bar on right
		self.editorCompilerSplitter = QtGui.QSplitter(self)
		mainLayout.addWidget(self.editorCompilerSplitter, 20)
		self.editorCompilerSplitter.setOrientation(QtCore.Qt.Horizontal)
		
		####################################################
		## Editor at top, Terminal at bottom Splitter
		self.editorTerminalSplitter = QtGui.QSplitter(self)
		self.editorTerminalSplitter.setOrientation(QtCore.Qt.Vertical)
		self.editorCompilerSplitter.addWidget(self.editorTerminalSplitter)

		#########################################
		## Editor Widget
		self.editor = EditorWidget(self, self.main)
		self.editorTerminalSplitter.addWidget(self.editor)

		#########################################
		## Terminal Widget
		self.terminalWidget = TerminalWidget(self, self.main)
		self.editorTerminalSplitter.addWidget(self.terminalWidget)
		

		##############################################################
		### Arduino Compiler Bar
		self.arduinoCompilerBar = ArduinoCompilerBar(self, self.main)
		self.connect(self.arduinoCompilerBar, QtCore.SIGNAL("compile_action"), self.on_compile_action)
		self.connect(self.arduinoCompilerBar, QtCore.SIGNAL("project_settings_changed"), self.on_project_settings_changed)

		self.editorCompilerSplitter.addWidget(self.arduinoCompilerBar)

		## Layout tweeks - TODO store thas in project
		self.editorCompilerSplitter.setStretchFactor(0, 2)
		self.editorCompilerSplitter.setStretchFactor(1, 0)
	
		self.editorTerminalSplitter.setStretchFactor(0, 5)
		self.editorTerminalSplitter.setStretchFactor(1, 2)


	##########################################
	## Load Project
	##########################################
	def load_project(self, project_file_path, tabIndex=None):
		# checks its a file, then laods editor
		## TODO - maybe check for .pde only

		self.project_file_path = None
		self.project_settings_file = None
		self.project_settings = None

		fileInfo = QtCore.QFileInfo(project_file_path)
		
		if fileInfo.isDir():
			self.emit(QtCore.SIGNAL("open_file"), None)
			self.editor.setText("")
			self.lblFileName.setText("")
			self.lblFileSize.setText("")
			self.lblFileModified.setText("")
			## TODO throw warning
			return

		self.project_file_path = fileInfo.filePath()

		self.project_settings_file = fileInfo.absolutePath().append("/project_settings.yaml")			
		self.load_project_settings()
		self.editor.load_file(self.project_file_path)
		self.arduinoCompilerBar.set_project(self.project_settings)



	##########################################
	## Compile Events
	##########################################
	def on_compile_action(self, compile_action):
		#print "on_compile_action", compile_action
		compiler = app.Compiler.Compiler(self)
		self.connect(compiler, QtCore.SIGNAL("compile_log"), self.terminalWidget.on_compile_log)
		compiler.ard_make(board = self.board, port=self.port, file_to_compile=self.current_file_path)

	def on_compiler_event(self):
		print "on_compiler_event"


	##########################################
	## Project Settings
	##########################################
	def on_project_settings_changed(self, new_project_settings):
		self.project_settings = new_project_settings
		self.save_project_settings()

	def save_project_settings(self):
		yaml_string = yaml.dump(self.project_settings, Dumper=Dumper, default_flow_style=False)
		app.utils.write_file(self.project_settings_file, yaml_string)
		print "project_settings_saved", self.project_settings, self.project_settings_file

	def load_project_settings(self):
		fileInfo = QtCore.QFileInfo(self.project_settings_file)
		if fileInfo.exists():
			self.project_settings =app.utils.load_yaml(self.project_settings_file)
		else:
			self.project_settings = None
		print "project_settings", self.project_settings