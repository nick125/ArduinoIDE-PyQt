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
		print main
		self.project_file_path = None
		self.board = None
		self.serial_port = None

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
		self.arduinoBar = ArduinoCompilerBar(self, self.main)
		self.connect(self.arduinoBar, QtCore.SIGNAL("compile_action"), self.on_compile_action)
		self.connect(self.arduinoBar, QtCore.SIGNAL("board_selected"), self.on_board_selected)
		self.connect(self.arduinoBar, QtCore.SIGNAL("serial_port_selected"), self.on_serial_port_selected)
		self.editorCompilerSplitter.addWidget(self.arduinoBar)

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
		self.editor.load_file(self.project_file_path)
		



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
	## Board/ serial Port Events
	##########################################
	def on_board_selected(self, board):
		self.board = board
		self.save_project_settings()

	def on_serial_port_selected(self, serial_port):
		self.serial_port = serial_port
		self.save_project_settings()


	##########################################
	## Project Settings
	##########################################
	def save_project_settings(self):
		dic = {'board': self.board, 'serial_port': self.serial_port}
		yaml_string = yaml.dump(dic, Dumper=Dumper, default_flow_style=False)
		settings_file = QtCore.QFileInfo(self.project_file_path).absolutePath().append("/project_settings.yaml")	
		app.utils.write_file(settings_file, yaml_string)

	def load_project_settings(self):
		print "ODO"