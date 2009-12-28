# -*- coding: utf-8 -*-


from PyQt4 import QtCore, QtGui
from PyQt4.Qsci import QsciScintilla, QsciAPIs
from PyQt4.Qsci import QsciLexerCPP, QsciLexerMakefile, QsciLexerJava, QsciLexerHTML, QsciLexerPerl, QsciLexerPython, QsciLexerYAML

from gui.EditorWidget import EditorWidget

from gui.icons import Ico 
from gui.icons import Icon 

class FileSystemBrowser(QtGui.QWidget):

	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self, parent)

		self.main = main

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setContentsMargins(0,0,0,0)
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

		source = self.main.ut.get_file_contents(fileInfo.filePath())
		## Allowed Extension
		if fileInfo.fileName() == 'Makefile':
			self.emit(QtCore.SIGNAL("open_file"), fileInfo.filePath())
			self.editor.set_source(source, 'Makefile' )
			#self.lexer = QsciLexerMakefile()
			#self.editor.setLexer(self.lexer)
			return

		extensions = ['java', 'html', 'py', 'pde', 'txt', 'yaml', 'sh', 'c','h','cpp','cxx', 'pl']
		if not fileInfo.suffix() in extensions:
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

		self.editor.set_source( txt, fileInfo.suffix())
		


#####################################################
## Tree Browser
#####################################################
class FileSystemTree(QtGui.QWidget):

	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self, parent)

		self.main = main
		self.model = QtGui.QDirModel(self)

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setContentsMargins(0,0,0,0)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)

		######################################################
		## Tree
		######################################################
		#toolbar = QtGui.QToolBar(self)
		#toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		#mainLayout.addWidget( toolbar )
		
		#self.comboPaths = QtGui.QComboBox()
		#toolbar.addWidget(self.comboPaths)
		#for path in self.main.settings.all_paths():
		#	self.comboPaths.addItem(path[1])
		

		self.treeBookmarks = QtGui.QTreeWidget(self)
		mainLayout.addWidget(self.treeBookmarks, 2)
		self.treeBookmarks.setRootIsDecorated(False)
		self.treeBookmarks.headerItem().setText(0, "Place")
		self.treeBookmarks.headerItem().setText(1, "Path")
		self.connect(self.treeBookmarks, QtCore.SIGNAL("itemDoubleClicked (QTreeWidgetItem *,int)"), self.on_bookmark_tree_double_clicked)
		self.connect(self.treeBookmarks, QtCore.SIGNAL("itemClicked (QTreeWidgetItem *,int)"), self.on_bookmark_tree_clicked)
		#self.tree.setModel(self.model)


		self.tree = QtGui.QTreeView(self)
		mainLayout.addWidget(self.tree, 5)
		self.tree.setModel(self.model)
		path = QtCore.QDir.currentPath() #(self.main.settings.app_path())
		self.tree.setRootIndex(self.model.index(path))
		self.connect(self.tree, QtCore.SIGNAL("clicked (const QModelIndex&)"), self.on_tree_clicked)
		#self.tree.setColumnWidth(0, 200)
		#self.tree.header().setStretchLastSection(True)
		self.tree.setColumnWidth(0, 150)
		self.tree.setColumnWidth(1, 50)
		self.tree.setColumnWidth(2, 50)
		self.tree.setColumnWidth(3, 50)
		for col in [1, 2, 3]:
			self.tree.setColumnHidden(col, True)

		###################################################
		## Bottom Select Column
		###################################################
		bottomBox = QtGui.QHBoxLayout()
		mainLayout.addLayout(bottomBox)

		self.showColumnButtonGroup = QtGui.QButtonGroup(self)
		self.showColumnButtonGroup.setExclusive(False)
		self.connect(self.showColumnButtonGroup, QtCore.SIGNAL("buttonClicked(QAbstractButton *)"), self.on_column_button_clicked)

		chk = QtGui.QCheckBox("Size")
		#chk.setChecked(True)
		bottomBox.addWidget(chk)
		self.showColumnButtonGroup.addButton(chk, 1)

		chk = QtGui.QCheckBox("Type")
		#chk.setChecked(True)
		bottomBox.addWidget(chk)
		self.showColumnButtonGroup.addButton(chk, 2)

		chk = QtGui.QCheckBox("Date Modified")
		#chk.setChecked(True)
		bottomBox.addWidget(chk)
		self.showColumnButtonGroup.addButton(chk, 3)
		

		self.load_bookmarks()

	def on_column_button_clicked(self, button):
		#if button.text() == "Size":
		col = self.showColumnButtonGroup.id(button)
		self.tree.setColumnHidden(col, not button.isChecked() )
		for col in range(0, 3):
			self.tree.resizeColumnToContents(col)

	def load_bookmarks(self):
		paths = self.main.settings.all_paths()
		for pathinfo in paths:
			item = QtGui.QTreeWidgetItem()
			item.setIcon(0, Icon(Ico.Folder))
			item.setText(0, pathinfo[0])
			item.setText(1, pathinfo[1])
			self.treeBookmarks.addTopLevelItem(item)


	def on_bookmark_tree_clicked(self, item, col):
		print "foo", item.text(1)
		path = item.text(1)
		self.tree.setRootIndex(self.model.index(path))


	def on_bookmark_tree_double_clicked(self, item, col):
		print "foo"


	def on_tree_clicked(self, modelIndex):
		
		file_path = self.model.filePath(modelIndex)
		fileInfo = QtCore.QFileInfo(file_path)
		#print fileInfo.filePath()
		self.emit(QtCore.SIGNAL("open_file"), fileInfo.filePath())