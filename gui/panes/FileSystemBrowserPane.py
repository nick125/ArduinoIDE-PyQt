# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.Qsci import QsciScintilla, QsciAPIs

from gui.widgets.EditorWidget import EditorWidget
from gui.widgets.FileSystemBrowserWidgets import FileSystemTree

import app.utils

from gui.icons import Ico 
from gui.icons import Icon 

class FileSystemBrowserPane(QtGui.QWidget):
	"""
		A pane to browse the filesystem
	"""
	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self, parent)

		self.main = main

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setContentsMargins(0, 0, 0, 0)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)
		splitter = QtGui.QSplitter()
		mainLayout.addWidget(splitter)	

		###################################################
		#### Toolbar
		#toolbar = QtGui.QToolBar(self)
		
		##
		leftLayout = QtGui.QVBoxLayout()
	
		###################################################
		#### Tree 
		self.tree = FileSystemTree(self, self.main)
		self.connect(self.tree, QtCore.SIGNAL("open_file"), self.on_open_file)
		splitter.addWidget(self.tree)

		###################################################
		#### Editor
		self.editor = EditorWidget(self, self.main, arduino_mode=False)
		splitter.addWidget(self.editor)
		#self.editor.setUtf8(True)
		#self.editor.setFolding(QsciScintilla.BoxedTreeFoldStyle)
		#self.setCentralWidget(self.editor)
		#self.editor.setMarginLineNumbers(1, True)
		#self.editor.setAutoIndent(True)

		splitter.setStretchFactor(0, 1)
		splitter.setStretchFactor(1, 2)
		

	def on_open_file(self, file_path):
		print "file_path", file_path
		#file_path = self.model.filePath(modelIndex)

		self.editor.load_file(file_path)
		return
		fileInfo = QtCore.QFileInfo(file_path)
		
		## check for directory
		if fileInfo.isDir():
			self.emit(QtCore.SIGNAL("open_file"), None)
			self.editor.setText("")
			return

		source = app.utils.get_file_contents(fileInfo.filePath())
		## Allowed Extension
		if fileInfo.fileName() == 'Makefile':
			self.emit(QtCore.SIGNAL("open_file"), fileInfo.filePath())
			self.editor.set_source(source, 'Makefile' )
			#self.lexer = QsciLexerMakefile()
			#self.editor.setLexer(self.lexer)
			return

		extensions = ['java', 'html', 'py', 'pde', 'txt', 'yaml', 'sh', 'c', 'h','cpp','cxx', 'pl']
		if not fileInfo.suffix() in extensions:
			self.emit(QtCore.SIGNAL("open_file"), None)
			self.editor.setText("")
			print "NOT SUPPORTED"
			return

		## load file
		txt = app.utils.get_file_contents(fileInfo.filePath())
		self.emit(QtCore.SIGNAL("open_file"), fileInfo.filePath())
		## TODO MAkefile and show images
		print "YES>>", fileInfo.suffix(), fileInfo.fileName(), fileInfo.filePath()

		self.editor.set_source( txt, fileInfo.suffix())
		
