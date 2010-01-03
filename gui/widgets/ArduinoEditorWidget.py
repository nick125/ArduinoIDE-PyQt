# -*- coding: utf-8 -*-

"""
The Arudino Editor contains  an 
* Editor
* Terminal Viewer
* Compiler Bar
"""

import os
from PyQt4 import QtCore, QtGui

#from PyQt4.Qsci import QsciScintilla, QsciAPIs
#from PyQt4.Qsci import QsciLexerCPP, QsciLexerMakefile, QsciLexerJava, QsciLexerHTML, QsciLexerPerl, QsciLexerPython, QsciLexerYAML

#from app.settings import settings
#import app.utils
#import app.Compiler

from gui.widgets import GenericWidgets
from gui.widgets.EditorWidget import EditorWidget
from gui.widgets.TerminalWidget import TerminalWidget
from gui.widgets.ArduinoCompilerBar import ArduinoCompilerBar

from gui.icons import Ico 
from gui.icons import Icon 

"""
extension_map = [
	(['makefile'], QsciLexerMakefile),
	(['pde', 'c', 'cpp', 'h'], QsciLexerCPP),
	(['py', 'pyw'], QsciLexerPython),
	(['htm', 'html'], QsciLexerHTML),
	(['pl',], QsciLexerPerl),
	(['java'], QsciLexerJava),
	(['yaml'], QsciLexerYAML),
]
"""
"""
### the current layout

=== File ===
Editor   | arduinocompiler
ternimal | ""



"""


class ArduinoEditorWidget(QtGui.QWidget):

	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self)

		self.main = main
		self.current_file_path = None
		self.board= "board_name"
		self.port = "Sanderman"

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
		self.editorCompilerSplitter.addWidget(self.arduinoBar)

		## Layout tweeks - TODO store thas in project
		self.editorCompilerSplitter.setStretchFactor(0, 2)
		self.editorCompilerSplitter.setStretchFactor(1, 0)
	
		self.editorTerminalSplitter.setStretchFactor(0, 5)
		self.editorTerminalSplitter.setStretchFactor(1, 2)

	def on_compile_action(self, compile_action):
		#print "on_compile_action", compile_action
		compiler = app.Compiler.Compiler(self)
		self.connect(compiler, QtCore.SIGNAL("compile_log"), self.terminalWidget.on_compile_log)
		compiler.ard_make(board = self.board, port=self.port, file_to_compile=self.current_file_path)

	def on_compiler_event(self):
		print "on_compiler_event"
		

	##########################################
	## Extensions
	##########################################
	## TODO - make this a list of allowed extension, we also need png and image viewer, xml etc in browser ?
	## nick what u think ?
	def supported(self):
		"""returns a list of supportes extensions"""
		extensions = [	'pde', 'c','h','cpp','cxx', 
						'java', 'py', 'pyw',  'pl', 'sh', 
						'html', 'yaml', 
						'txt'
					]
		return extensions

	def ignored(self):
		"""returns a list of ignored extensions""" ## TODO - image viewer
		extensions = [	'pyc', 'png','gif','jpeg' ]
		return extensions





	def on_upload(self):
		print "upload"


	def DEADload_keywords(self):
		words_file = settings.keywords_path().absoluteFilePath("/keywords_ripped.txt")
		words_str = app.utils.get_file_contents(words_file)
		word_lines = words_str.split("\n")
		for line in word_lines:
			#print line
			line = line.trimmed()
			#print "..", line
			if line.length() > 0:
				if not line.startsWith("#"):
					line = str(line)
					parts = line.split(" ")
					#print parts
					for p in parts:
						print "==", p
					keyword = parts[0]
					print "#%s#" % keyword
					self.arduinoFunctionsAPI.add(keyword)


	def find_lexer(self, extension):
		extension = extension.toLower()
		#TODO: This is horrible and evil. Fix it.
		for extensions, lexer in extension_map:
			if extension in extensions:
				return lexer()
		# Fallback
		return QsciLexerCPP()

	def set_source(self, source, extension=None):

		self.editor.setText(source)
		self.lexer = self.find_lexer(extension)
		self.editor.setLexer(self.lexer)

	def load_file(self, file_path, tabIndex=None):
		print "file_path", file_path
		fileInfo = QtCore.QFileInfo(file_path)
		return
		if fileInfo.isDir():
			#self.emit(QtCore.SIGNAL("open_file"), None)
			self.editor.setText("")
			self.lblFileName.setText("")
			self.lblFileSize.setText("")
			self.lblFileModified.setText("")
			self.current_file_path = None
			return

		self.current_file_path = fileInfo.filePath()
		file_name_string = QtCore.QString("<b>").append(fileInfo.fileName()).append("</b>")
		self.lblFileName.setText(file_name_string)
		self.lblFileSize.setText("%sB" % fileInfo.size())
		self.lblFileModified.setText("%s" % fileInfo.lastModified().toString(QtCore.Qt.SystemLocaleShortDate))
		source = app.utils.get_file_contents(fileInfo.filePath())

		## unique Files
		if fileInfo.fileName() == 'Makefile':
			self.set_source(source, 'Makefile' )
			return

		## Ignored extension
		if fileInfo.suffix() in self.ignored():
			file_name_string.append("  <small> *** ignored ***</small>")
			self.lblFileName.setText(file_name_string)
			self.editor.setText("")
			return
		
		if not fileInfo.suffix() in self.supported():
			file_name_string.append("  <small> *** not supported ***</small>")		
			self.lblFileName.setText(file_name_string)
			self.editor.setText("")
			return

		## load file
		txt = app.utils.get_file_contents(fileInfo.filePath())
		self.emit(QtCore.SIGNAL("open_file"), fileInfo.filePath())
		#self.editor.set_source(txt)
			## QsciLexerCPP, QsciLexerMakefile, QsciLexerJava, QsciLexerHTML, QsciLexerPerl, QsciLexerPython, QsciLexerYAML
		## TODO MAkefile and show images
		print "YES>>", fileInfo.suffix(), fileInfo.fileName(), fileInfo.filePath()

		self.set_source( txt, fileInfo.suffix())

	######################################################################
	## Write File
	######################################################################
	def write_file(self):
		file2Write = QtCore.QFile(self.current_file_path)
		if not file2Write.open(QtCore.QIODevice.WriteOnly | QtCore.QIODevice.Text):
			print "TODO: error writing file"
			return
		stream_out = QtCore.QTextStream(file2Write)
		stream_out << self.editor.text()
		file2Write.close()

