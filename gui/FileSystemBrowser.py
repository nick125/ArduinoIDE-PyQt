# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.Qsci import QsciScintilla, QsciAPIs

from gui.icons import Ico 
from gui.icons import Icon 

class FileSystemBrowser(QtGui.QWidget):

	
	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self, parent)

		self.main = main

		mainLayout = QtGui.QHBoxLayout()
		self.setLayout(mainLayout)
		splitter = QtGui.QSplitter()
		mainLayout.addWidget(splitter)
		
		self.model = QtGui.QDirModel(self)
	
		###################################################
		#### Tree 
		self.tree = QtGui.QTreeView(self)
		splitter.addWidget(self.tree)
		self.tree.setModel(self.model)
		path = QtCore.QDir.currentPath() #(self.main.settings.app_path())
		self.tree.setRootIndex(self.model.index(path))

		###################################################
		#### Editor
		self.editor = QsciScintilla(self)
		splitter.addWidget(self.editor)
		self.editor.setUtf8(True)
		self.editor.setFolding(QsciScintilla.BoxedTreeFoldStyle)
		#self.setCentralWidget(self.editor)
		self.editor.setMarginLineNumbers(1, True)
		self.editor.setAutoIndent(True)
		