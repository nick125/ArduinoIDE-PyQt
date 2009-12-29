# -*- coding: utf-8 -*-

import os
from PyQt4 import QtCore, QtGui

from PyQt4.Qsci import QsciScintilla, QsciAPIs
from PyQt4.Qsci import QsciLexerCPP, QsciLexerMakefile, QsciLexerJava, QsciLexerHTML, QsciLexerPerl, QsciLexerPython, QsciLexerYAML

import gui.widgets
from gui.TerminalWidget import TerminalWidget
from gui.icons import Ico 
from gui.icons import Icon 

extension_map = [
	(['makefile'], QsciLexerMakefile),
	(['pde', 'c', 'cpp', 'h'], QsciLexerCPP),
	(['py', 'pyw'], QsciLexerPython),
	(['htm', 'html'], QsciLexerHTML),
	(['pl',], QsciLexerPerl),
	(['java'], QsciLexerJava),
	(['yaml'], QsciLexerYAML),
]

class EditorWidget(QtGui.QWidget):

	def __init__(self, parent, main, arduino_mode=False):
		QtGui.QWidget.__init__(self)

		self.main = main
		self.current_file_path = None

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setContentsMargins(0, 0, 0, 0)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)

		##############################################################
		### File Info Bar
		##############################################################
		hbox = QtGui.QHBoxLayout()
		mainLayout.addLayout(hbox)

		self.lblFileName = QtGui.QLabel(self)
		self.lblFileName.setText("Filename")
		style_grad = "background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #efefef, stop: 1 %s);" % "#6A7885"
		style_grad += "font-weight: bold; border: 1px outset #41484E; padding: 3px;"
		self.lblFileName.setStyleSheet(style_grad)
		hbox.addWidget(self.lblFileName, 4)

		self.lblFileSize = gui.widgets.StatusLabel(self, "Size")
		hbox.addWidget(self.lblFileSize, 1)

		self.lblFileModified = gui.widgets.StatusLabel(self, "Modified")
		hbox.addWidget(self.lblFileModified, 2)

		##############################################################
		### Arduino Compiler
		##############################################################
		if arduino_mode:
			toolbar = QtGui.QToolBar()
			toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
			mainLayout.addWidget(toolbar)

			## spacer for right
			toolbar.addWidget(gui.widgets.ToolBarSpacer(self))

			### Action Buttons
			buttz = []
			buttz.append(['Compile', Ico.Compile])
			buttz.append(['Upload', Ico.Upload])
			buttz.append(['Compile Upload', Ico.CompileUpload])
			self.buttCompileGroup = QtGui.QButtonGroup()
			self.connect(self.buttCompileGroup, QtCore.SIGNAL("buttonClicked (QAbstractButton *)"), self.on_compile_group_button)
			## TODO connect
			for caption, ico in buttz:
				butt = QtGui.QPushButton()
				butt.setText(caption)
				butt.setIcon(Icon(ico))
				toolbar.addWidget(butt)
				self.buttCompileGroup.addButton(butt)
			toolbar.addSeparator()
		
	
		####################################################
		## Source Editor
		####################################################
		self.editor = QsciScintilla(self)
		self.editor.setUtf8(True)
		self.editor.setFolding(QsciScintilla.BoxedTreeFoldStyle)
		self.editor.setMarginLineNumbers(1, True)
		self.editor.setAutoIndent(True)
		mainLayout.addWidget(self.editor, 3)



		## The Syntax Higlighter = standard CPP atmo = cish
		#self.lexer = ArduinoLexer(self)
		#self.editor.setLexer(self.lexer)
	
		## Aarduino API Functions
		#self.arduinoFunctionsAPI = QsciAPIs(self.lexer)
		#keywords_file = self.main.settings.api_path().append("/autocomplete.txt")

		#self.arduinoFunctionsAPI.load(keywords_file)
		#self.arduinoFunctionsAPI.prepare()
		#self.lexer.setAPIs(self.arduinoFunctionsAPI)

		#self.editor.setAutoCompletionThreshold(1);
		#self.editor.setAutoCompletionSource(QsciScintilla.AcsAPIs);
	
		if arduino_mode:
			self.terminalWidget = TerminalWidget(self, self.main)
			mainLayout.addWidget(self.terminalWidget, 1)


	##########################################
	## Extensions
	##########################################
	def supported(self):
		"""returns a list of supportes extensions"""
		extensions = [	'pde', 'c','h','cpp','cxx', 
						'java', 'py',  'pl', 'sh', 
						'html', 'yaml', 
						'txt'
					]
		return extensions

	def ignored(self):
		"""returns a list of ignored extensions""" ## TODO - image viewer
		extensions = [	'pyc', 'png','gif','jpeg' ]
		return extensions

	##########################################
	## Compile Upload Buttons
	##########################################	
	def on_compile_group_button(self, butt):
		print "COMP", butt.text()
		if butt.text() == "Compile":
			self.write_file()
			self.compile_file()
		else:
			self.main.status.showMessage("Not recognised", 4000)

	def compile_file(self):
		self.terminalWidget.compile(self.current_file_path)





	def on_upload(self):
		print "upload"


	def load_keywords(self):
		words_file = self.main.settings.keywords_path().append("/keywords_ripped.txt")
		words_str = self.main.ut.get_file_contents(words_file)
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
		self.lblFileSize.setText("%s" % fileInfo.size())
		self.lblFileModified.setText("%s" % fileInfo.lastModified().toString(QtCore.Qt.SystemLocaleShortDate))
		source = self.main.ut.get_file_contents(fileInfo.filePath())

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
		txt = self.main.ut.get_file_contents(fileInfo.filePath())
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

