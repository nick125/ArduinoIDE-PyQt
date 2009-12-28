# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from PyQt4.Qsci import QsciScintilla, QsciAPIs
from PyQt4.Qsci import QsciLexerCPP, QsciLexerMakefile, QsciLexerJava, QsciLexerHTML, QsciLexerPerl, QsciLexerPython, QsciLexerYAML

import gui.widgets
from gui.TerminalWidget import TerminalWidget
from gui.icons import Ico 
from gui.icons import Icon 


class EditorWidget(QtGui.QWidget):

	def __init__(self, parent, main, arduino_mode=False):
		QtGui.QWidget.__init__(self)

		self.main = main
		self.current_file_path = None

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setContentsMargins(0,0,0,0)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)


		### File Info Bar
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


		if arduino_mode:
			toolbar = QtGui.QToolBar()
			toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
			mainLayout.addWidget(toolbar)

			### Action Buttons
			self.actionCompile = toolbar.addAction(Icon(Ico.Compile), "Save and Compile", self.on_compile)
			self.chkAutoUpload = QtGui.QCheckBox("Upload after compile")
			self.chkAutoUpload.setCheckState(QtCore.Qt.Checked)
			toolbar.addWidget(self.chkAutoUpload)
			self.actionUpload = toolbar.addAction(Icon(Ico.Upload), "Upload", self.on_upload)
			#self.actionCompile.setIcon(Icon(Ico.Compile))
			#self.actionCompile.setText("Compile")
			#toolbar.addWidget(
			#, self.on_compile)
		
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


	def supported(self):
		extensions = [	'pde', 'c','h','cpp','cxx', 
						'java', 'py',  'pl', 'sh', 
						'html', 'yaml', 
						'txt'
					]
		return extensions

	def ignored(self):
		extensions = [	'pyc', 'png','gif','jpeg' ]
		return extensions

	def write_file(self):
		file2Write = QtCore.QFile(self.current_file_path)
		if not file2Write.open(QtCore.QIODevice.WriteOnly | QtCore.QIODevice.Text):
			print "TODO: error writing file"
			return
		stream_out = QtCore.QTextStream(file2Write)
		stream_out << self.editor.text()
		file2Write.close()


	def on_compile(self):
		print "compile"
		self.write_file()
		self.compile_file()


	def compile_file(self):
		command = "ls -all"
		



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


	def set_source(self, source, suffix=None):

		self.editor.setText(source)

		if suffix in ['cpp', 'c', 'h','cxx', 'pde']:
			self.lexer = QsciLexerCPP()
			
		elif suffix == 'java':
			self.lexer = QsciLexerJava()

		elif suffix == 'html':
			self.lexer = QsciLexerHTML()

		elif suffix == 'pl':
			self.lexer = QsciLexerPerl()

		elif suffix == 'py':
			self.lexer = QsciLexerPython()

		elif suffix == 'sh':
			self.lexer = QsciLexerBash()

		elif suffix == 'yaml':
			self.lexer = QsciLexerYAML()

		else:
			#TODO unsupported Highlighter and text file
			self.lexer = QsciLexerCPP()


		self.editor.setLexer(self.lexer)


	def load_file(self, file_path):
		

		fileInfo = QtCore.QFileInfo(file_path)

		if fileInfo.isDir():
			#self.emit(QtCore.SIGNAL("open_file"), None)
			self.editor.setText("")
			print "Directory"
			self.lblFileName.setText("")
			self.lblFileName.setText("")
			return

		file_name_string = QtCore.QString("<b>").append(fileInfo.fileName()).append("</b>")
		self.lblFileName.setText(file_name_string)
		self.lblFileSize.setText("%s" % fileInfo.size())
		self.lblFileModified.setText("%s" % fileInfo.lastModified().toString(QtCore.Qt.SystemLocaleShortDate))

		source = self.main.ut.get_file_contents(fileInfo.filePath())

		## unique Files
		if fileInfo.fileName() == 'Makefile':
			print "MAKEFILE"
			self.set_source(source, 'Makefile' )
			return

		## Ignored extension
		if fileInfo.suffix() in self.ignored():
			print "Ignored: ", fileInfo.suffix()
			file_name_string.append("  <small> *** ignored ***</small>")
			self.lblFileName.setText(file_name_string)
			return
		
		if not fileInfo.suffix() in self.supported():
			self.emit(QtCore.SIGNAL("open_file"), None)
			self.editor.setText("")
			print "NOT SUPPORTED"
			return

		## load file
		txt = self.main.ut.get_file_contents(fileInfo.filePath())
		self.emit(QtCore.SIGNAL("open_file"), fileInfo.filePath())
		#self.editor.set_source(txt)
			## QsciLexerCPP, QsciLexerMakefile, QsciLexerJava, QsciLexerHTML, QsciLexerPerl, QsciLexerPython, QsciLexerYAML
		## TODO MAkefile and show images
		print "YES>>", fileInfo.suffix(), fileInfo.fileName(), fileInfo.filePath()

		self.set_source( txt, fileInfo.suffix())
