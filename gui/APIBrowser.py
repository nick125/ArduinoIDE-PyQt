# -*- coding: utf-8 -*-

import yaml
from PyQt4 import QtCore, QtGui

from gui.FunctionEditDialog import FunctionEditDialog
from gui.icons import Ico 
from gui.icons import Icon 



class SSHelpDockWidget(QtGui.QDockWidget):

	
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



class APIBrowser(QtGui.QWidget):

	class COLS:
		icon = 0
		desc = 1
		parap = 2
		section = 3
		function = 4
	
	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self)

		self.main = main

		layout = QtGui.QVBoxLayout()
		layout.setContentsMargins(0,0,0,0)
		layout.setSpacing(0)
		self.setLayout(layout)

		#headLabel = gui.widgets.HeaderLabel(self, self.main, icon=Ico.Help, title="Help", color="blue", wash_to="yellow")
		#layout.addWidget(headLabel)


		###########################
		### Toolbar
		toolbar = QtGui.QToolBar()
		toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		layout.addWidget( toolbar )
		
		actionAdd = toolbar.addAction(Icon(Ico.FunctionAdd), "Add Function", self.on_add_function)
		self.actionAdd = toolbar.addAction(Icon(Ico.FunctionAdd), "Edit Function", self.on_edit_function)


		#headerLayout.addWidget(lblTitle)
		toolbar.addWidget(QtGui.QLabel("Filter:"))
		self.txtFilter = QtGui.QLineEdit()
		toolbar.addWidget(self.txtFilter)

		

		self.tree = QtGui.QTreeWidget()
		self.tree.setRootIsDecorated(True)
		self.tree.setAlternatingRowColors(True)
		layout.addWidget(self.tree)
		self.connect(self.tree, QtCore.SIGNAL("itemDoubleClicked (QTreeWidgetItem *,int)"), self.on_tree_double_clicked)

		self.tree.headerItem().setText(self.COLS.icon, "Function")
		self.tree.headerItem().setText(1, "Paramaters")
		self.tree.headerItem().setText(2, "Description")
		self.tree.headerItem().setText(self.COLS.section, "Section")
		self.tree.headerItem().setText(self.COLS.function, "Function")
		self.tree.header().setStretchLastSection(True)
		self.tree.setColumnWidth(0, 300)

		self.load()

	def on_add_function(self):
		d = gui.FunctionEditDialog.FunctionEditDialog(self, self.main)
		d.show()

	def on_edit_function(self):
		pass

	##################################################
	## LOAD
	##################################################
	def load(self):
		path = self.main.settings.def_path()
		#print path
		di = QtCore.QDir(path)
		for entry in di.entryInfoList(QtCore.QDir.AllEntries | QtCore.QDir.NoDotAndDotDot):
			#print "E========", entry.filePath(), entry.fileName()
			dirItem = QtGui.QTreeWidgetItem()
			dirItem.setText(self.COLS.icon, entry.fileName())
			dirItem.setIcon(self.COLS.icon, Icon(Ico.Folder))
			dirItem.setData(self.COLS.icon, QtCore.Qt.UserRole, QtCore.QVariant(entry.filePath()))
			dirItem.setFirstColumnSpanned(True)
			self.tree.addTopLevelItem(dirItem)
			self.tree.setItemExpanded(dirItem, True)
			sub_dir = QtCore.QDir(entry.filePath())
			for sub_entry in sub_dir.entryInfoList(QtCore.QDir.AllEntries | QtCore.QDir.NoDotAndDotDot):
				#print sub_entry.fileName()
				
				## load api
				api = self.main.ut.load_yaml(sub_entry.filePath())
				#print api
				funkFileItem = QtGui.QTreeWidgetItem(dirItem)
				funkFileItem.setIcon(self.COLS.icon, Icon(Ico.Function))
				funkFileItem.setText(self.COLS.icon, sub_entry.fileName())
				funkFileItem.setText(self.COLS.icon, api['syntax'])
				funkFileItem.setText(self.COLS.function, api['function'])
				funkFileItem.setData(self.COLS.icon, QtCore.Qt.UserRole, QtCore.QVariant(sub_entry.filePath()))
				
				#dirItem.setData(0, entry.filePath())
				#dirItem.setFirstColumnSpanned(True)
				#self.tree.addTopLevelItem(dirItem)


	def on_tree_double_clicked(self, item, column):
		#print item, column
		#print item.text(0), item.data(0, QtCore.Qt.UserRole).toString()
		if item.text(self.COLS.function).length() > 0:
			print "its a function"
		file_path = item.data(self.COLS.icon, QtCore.Qt.UserRole).toString()
		dialog = FunctionEditDialog(self, self.main, function_file=file_path)
		dialog.show()