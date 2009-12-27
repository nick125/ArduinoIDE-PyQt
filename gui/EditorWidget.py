# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from PyQt4.Qsci import QsciScintilla, QsciAPIs

from gui.Lexer import ArduinoLexer
from gui.TerminalWidget import TerminalWidget
from gui.icons import Ico 
from gui.icons import Icon 

class EditorWidget(QtGui.QWidget):

	def __init__(self, main):
		QtGui.QWidget.__init__(self)

		self.main = main
		self.current_file_path = None

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setContentsMargins(0,0,0,0)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)

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
		#self.setCentralWidget(self.editor)
		self.editor.setMarginLineNumbers(1, True)
		self.editor.setAutoIndent(True)
		mainLayout.addWidget(self.editor, 3)

		#lex = QsciLexerCustom()

		#apis = QsciAPIs(lex);
		#apis.add("test");
		#apis.add("test123");
		#apis.add("foobar");
		#apis.prepare();
		#lex.setAPIs(apis);

		## The Syntax Higlighter = standard CPP atmo = cish
		self.lexer = ArduinoLexer(self)
		self.editor.setLexer(self.lexer)
	
		## Aarduino API Functions
		self.arduinoFunctionsAPI = QsciAPIs(self.lexer)
		keywords_file = self.main.settings.keywords_path().append("/arduino.txt")
		#print keywords_file
		self.arduinoFunctionsAPI.load(keywords_file)
		self.load_keywords()
		"""self.arduinoFunctionsAPI.add("INPUT")
		self.arduinoFunctionsAPI.add("OUTPUT")
		self.arduinoFunctionsAPI.add("DEFAULT")
		self.arduinoFunctionsAPI.add("OUTPUT")
		self.arduinoFunctionsAPI.add("LOW")
		self.arduinoFunctionsAPI.add("HIGH")
		"""
		self.arduinoFunctionsAPI.prepare()
		self.lexer.setAPIs(self.arduinoFunctionsAPI)

		## Aarduino Constants
		"""
		aarduinoContantsAPI = QsciAPIs(self.lexer)
		keywords_file = self.main.settings.keywords_path().append("/constants.txt")
		#print keywords_file
		aarduinoContantsAPI.load(keywords_file)
		aarduinoContantsAPI.prepare()
		self.lexer.setAPIs(aarduinoContantsAPI)
		"""	
		self.editor.setAutoCompletionThreshold(1);
		self.editor.setAutoCompletionSource(QsciScintilla.AcsAPIs);
	

		self.terminalWidget = TerminalWidget(self, self.main)
		mainLayout.addWidget(self.terminalWidget, 1)


	def open_file(self, file_path=None):
		
		self.current_file_path = file_path
		source = self.main.ut.get_file_contents(self.current_file_path)
		# self.emit(QtCore.SIGNAL("source_loaded"), source)
		self.editor.setText(source)

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
