# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from PyQt4.Qsci import QsciScintilla, QsciAPIs

from gui.Lexer import ArduinoLexer

from gui.icons import Ico 
from gui.icons import Icon 

class EditorWidget(QtGui.QWidget):

	def __init__(self, main):
		QtGui.QWidget.__init__(self)

		self.main = main

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setContentsMargins(0,0,0,0)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)

		toolbar = QtGui.QToolBar()
		toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		mainLayout.addWidget(toolbar)

		### Action Buttons
		self.actionCompile = toolbar.addAction(Icon(Ico.Compile), "Compile", self.on_compile)
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
		#self.setCentralWidget(self.editor)
		self.editor.setMarginLineNumbers(1, True)
		self.editor.setAutoIndent(True)
		mainLayout.addWidget(self.editor)

		#lex = QsciLexerCustom()

		#apis = QsciAPIs(lex);
		#apis.add("test");
		#apis.add("test123");
		#apis.add("foobar");
		#apis.prepare();
		#lex.setAPIs(apis);

		#self.editor.setLexer(lex)
		self.lexer = ArduinoLexer(self)
		self.editor.setLexer(self.lexer)
	
		apis = QsciAPIs(self.lexer)
		apis.add("INPUT")
		apis.add("OUTPUT")
		apis.add("foobar")
		apis.prepare()
		self.lexer.setAPIs(apis)
		self.editor.setAutoCompletionThreshold(2);
		self.editor.setAutoCompletionSource(QsciScintilla.AcsAPIs);
	

	def set_source(self, source):
		self.editor.setText(source)

	def load_file(self):
		print "load_file"


	def on_compile(self):
		print "compile"

	def on_upload(self):
		print "upload"



