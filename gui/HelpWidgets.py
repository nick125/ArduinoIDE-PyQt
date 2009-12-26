# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from gui.HelpBrowser import HelpBrowserDialog

from gui.icons import Ico 
from gui.icons import Icon 

import gui.widgets

class HelpDockWidget(QtGui.QDockWidget):

	
	def __init__(self, parent, main):
		QtGui.QDockWidget.__init__(self)

		self.main = main

		containerWidget = QtGui.QWidget()
		self.setWidget(containerWidget)

		layout = QtGui.QVBoxLayout()
		layout.setContentsMargins(0,0,0,0)
		layout.setSpacing(0)
		containerWidget.setLayout(layout)	

		helpWidget = HelpWidget(self, self.main)
		layout.addWidget(helpWidget)



class HelpWidget(QtGui.QWidget):

	
	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self)

		self.main = main

		layout = QtGui.QVBoxLayout()
		layout.setContentsMargins(0,0,0,0)
		layout.setSpacing(0)
		self.setLayout(layout)

		headLabel = gui.widgets.HeaderLabel(self, self.main, icon=Ico.Help, title="Help", color="blue", wash_to="yellow")
		layout.addWidget(headLabel)


		###########################
		### Toolbar
		toolbar = QtGui.QToolBar()
		toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		layout.addWidget( toolbar )
		
	
		#headerLayout.addWidget(lblTitle)
		toolbar.addWidget(QtGui.QLabel("Filter:"))
		self.txtFilter = QtGui.QLineEdit()
		toolbar.addWidget(self.txtFilter)

		

		self.tree = QtGui.QTreeWidget()
		self.tree.setRootIsDecorated(False)
		self.tree.setAlternatingRowColors(True)
		layout.addWidget(self.tree)
		self.connect(self.tree, QtCore.SIGNAL("itemDoubleClicked (QTreeWidgetItem *,int)"), self.on_tree_double_clicked)

		self.tree.headerItem().setText(0, "Topic")

		self.load_files()

	def load_files(self):
		pathStr = self.main.settings.help_path()
		dirr = QtCore.QDir(pathStr)
		if not dirr.exists():
			QtGui.QMessageBox.information(self, "OOps", " the reference dir %s was not found" % pathStr)
			return
		## TODO - make this return *.html
		infoList = dirr.entryInfoList(QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot)
		for fileInfo in infoList:
			if fileInfo.suffix() == 'html':
				treeItem = QtGui.QTreeWidgetItem()
				treeItem.setText(0, fileInfo.baseName() ) ## hack to remove .html
				treeItem.setData(0, QtCore.Qt.UserRole, QtCore.QVariant( fileInfo.filePath() ))
				treeItem.setIcon(0, Icon(Ico.HelpDoc))
				self.tree.addTopLevelItem(treeItem)

	def on_tree_double_clicked(self, item, column):
		#print item, column
		#print item.text(0), item.data(0, QtCore.Qt.UserRole).toString()
		dialog = HelpBrowserDialog(self, self.main)
		dialog.load_help_page( item.data(0, QtCore.Qt.UserRole).toString() )
		dialog.show()