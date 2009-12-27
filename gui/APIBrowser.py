# -*- coding: utf-8 -*-

import yaml
from PyQt4 import QtCore, QtGui

from gui.FunctionEditDialog import FunctionEditDialog
from gui.FileDialogs import FolderEditDialog
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
		description = 1
		section = 2
		function = 3
		folder = 4
	
	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self)

		self.main = main
		self.paths = None

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

		act = toolbar.addAction(Icon(Ico.Refresh), "Refresh", self.on_refresh)
		self.chkExtendedNodes = QtGui.QCheckBox("Show vars")
		toolbar.addWidget(self.chkExtendedNodes)
		self.connect(self.chkExtendedNodes, QtCore.SIGNAL("clicked()"), self.on_refresh)
		toolbar.addSeparator()
		
		self.actionAddFunction = toolbar.addAction(Icon(Ico.FunctionAdd), "Add Function", self.on_add_function)
		#self.actionAddFunction.setDisabled(True)

		self.actionEditFunction = toolbar.addAction(Icon(Ico.FunctionEdit), "Edit Function", self.on_edit_function)
		self.actionEditFunction.setDisabled(True)

		self.actionDeleteFunction = toolbar.addAction(Icon(Ico.FunctionDelete), "Delete Function", self.on_delete_function)
		self.actionDeleteFunction.setDisabled(True)
		toolbar.addSeparator()

		self.folderactionGroup = QtGui.QActionGroup(self)
		self.folderactionGroup.setDisabled(True)

		self.actionAddFolder = toolbar.addAction(Icon(Ico.FolderAdd), "Create", self.on_add_folder)
		self.folderactionGroup.addAction(self.actionAddFolder)

		self.actionEditFolder = toolbar.addAction(Icon(Ico.FolderEdit), "Rename", self.on_edit_folder)
		self.folderactionGroup.addAction(self.actionEditFolder)

		self.actionDeleteFolder = toolbar.addAction(Icon(Ico.FolderDelete), "Delete", self.on_delete_folder)
		self.folderactionGroup.addAction(self.actionDeleteFolder)
		toolbar.addSeparator()

		self.actionWriteApiFile = toolbar.addAction(Icon(Ico.WriteFile), "Write API file", self.on_write_api_file)

		
		#toolbar.addWidget(self.chkExtendedNodes)
		#headerLayout.addWidget(lblTitle)
		#toolbar.addWidget(QtGui.QLabel("Filter:"))
		#self.txtFilter = QtGui.QLineEdit()
		#toolbar.addWidget(self.txtFilter)

		

		self.tree = QtGui.QTreeWidget()
		self.tree.setRootIsDecorated(True)
		self.tree.setAlternatingRowColors(True)
		layout.addWidget(self.tree)
		self.connect(self.tree, QtCore.SIGNAL("itemDoubleClicked (QTreeWidgetItem *,int)"), self.on_tree_item_double_clicked)
		self.connect(self.tree, QtCore.SIGNAL("itemClicked (QTreeWidgetItem *,int)"), self.on_tree_item_clicked)

		self.tree.headerItem().setText(self.COLS.icon, "Function")
		self.tree.headerItem().setText(self.COLS.description, "Description")
		#self.tree.headerItem().setText(2, "Description")
		self.tree.headerItem().setText(self.COLS.section, "Section")
		self.tree.headerItem().setText(self.COLS.function, "Function")
		self.tree.headerItem().setText(self.COLS.folder, "Folder")
		self.tree.header().setStretchLastSection(True)
		self.tree.setColumnWidth(0, 300)

		self.api_lines = None
		self.load()

	def on_write_api_file(self):
		rootItem = self.tree.invisibleRootItem()
		self.api_lines = []
		print "write-api-----------------------------------------------"
		self.extract_api(rootItem)
		for l in self.api_lines:
			print l
		api_string = "\n".join(self.api_lines)
		file_path = self.main.settings.def_path().append("/autocomplete.txt")
		#print file_path
		self.main.ut.write_file(file_path, api_string)

	def extract_api(self, treeItem):
		#print "extract"
		if treeItem.childCount() > 0:
			for idx in range(0, treeItem.childCount()):
				item = treeItem.child(idx)
				#print item
				if item.text(self.COLS.function).length() > 0:
					file_path = item.data(self.COLS.icon, QtCore.Qt.UserRole).toString()
					api = self.main.ut.load_yaml(file_path)
					#for a in api:
						#print a
					#api_str = ''
					if 'parameters_type' in api and api['parameters_type'] == 'variable':
						func_name = str(api['function'])
						if func_name.find(".") > 1:
							self.api_lines.append(api['function'] + "()")
							func_name = api['function'].split(".")[1]
							#func_name
							#self.api_lines.append(api_str)
							#func_name = api['function']
						for dic in api['parameters']:
							api_str = func_name
							api_str = api_str + "(" + dic.keys()[0] + ") " + api['summary']
							self.api_lines.append(api_str)

					else:
						api_str = api['function']
						l = []
						for dic in api['parameters']:
							l.append(dic.keys()[0]) #, dic.values()[0]
						api_str += "(" + ", ".join(l) + ") " #+ dic.values()[0]
						self.api_lines.append(api_str)
							
				else:
					self.extract_api(item)

	##################################################
	## Function Actions
	##################################################

	def on_add_function(self):
		path = self.tree.currentItem().text(self.COLS.folder)
		d = FunctionEditDialog(self, self.main, None, path, self.paths )
		d.show()
		self.load()

	def on_edit_function(self):
		path = self.tree.currentItem().text(self.COLS.folder)
		fileinfo = QtCore.QFileInfo(self.tree.currentItem().data(self.COLS.icon, QtCore.Qt.UserRole).toString())
		d = FunctionEditDialog(self, self.main, fileinfo.fileName(), path, self.paths )
		d.show()
		self.load()

	def on_delete_function(self):
		item = self.tree.currentItem()
		msg = QtCore.QString("Delete the function\n").append(item.text(self.COLS.icon))
		resp = QtGui.QMessageBox.question(self, "Confirm Delete Function", msg, QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		if resp == QtGui.QMessageBox.Yes:
			file_path = item.data(self.COLS.icon, QtCore.Qt.UserRole).toString()
			ok = QtCore.QFile.remove(file_path)
			self.load()

	##################################################
	## Folder Actions
	##################################################

	def on_add_folder(self):
		parent_folder = self.tree.currentItem().text(self.COLS.folder)

		txt, ok = QtGui.QInputDialog.getText(self, "New Folder",
                                          "Create folder under %s" % parent_folder, QtGui.QLineEdit.Normal,
                                          "foo")
		if ok:
			#dir_str = parent_folder.append(txt)
			pth = self.main.settings.def_path().append(parent_folder)
			print pth
			dirr = QtCore.QDir(pth)
			success = dirr.mkdir(txt)
			if success:
				self.load()
			else:
				print "error" # TODO

     #if (ok && !text.isEmpty())
      #   textLabel->setText(text);

		#dialog = FolderEditDialog(self, self.main, folder, parent=parent_folder)
		#dialog.exec_()

	def on_edit_folder(self):
		folder = self.tree.currentItem().data(self.COLS.icon, QtCore.Qt.UserRole).toString()
		#print folder
		dialog = FolderEditDialog(self, self.main, folder)
		if dialog.exec_():
			self.load()
	
	def on_delete_folder(self):
		pass

	def on_refresh(self):
		self.load()

	##################################################
	## LOAD
	##################################################
	def load(self):


		self.tree.model().removeRows(0, self.tree.model().rowCount())
		rootNode = self.tree.invisibleRootItem()
		root_path = self.main.settings.def_path()
		rootDir = QtCore.QDir(root_path)
		self.paths = []
		self.walk_dir(rootDir, '/', rootNode)

	def walk_dir(self, sub_dir, folder, parentItem):
	
		for file_entry in sub_dir.entryInfoList(QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot):
			if file_entry.suffix() == 'yaml':
				self.add_yaml_function_node(file_entry, folder, parentItem)
	
		for folder_entry in sub_dir.entryInfoList(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot):
			n_folder = folder + folder_entry.fileName() + "/"
			dirItem = QtGui.QTreeWidgetItem(parentItem)
			dirItem.setText(self.COLS.icon, folder_entry.fileName())
			dirItem.setText(self.COLS.folder, n_folder)
			dirItem.setIcon(self.COLS.icon, Icon(Ico.Folder))
			dirItem.setData(self.COLS.icon, QtCore.Qt.UserRole, QtCore.QVariant(folder_entry.filePath()))
			dirItem.setFirstColumnSpanned(False)
			self.tree.setItemExpanded(dirItem, True)

			self.walk_dir(QtCore.QDir(folder_entry.filePath()), n_folder, dirItem)
			self.paths.append( str(n_folder) )
		
	def add_yaml_function_node(self, sub_entry, folder, parentNode):
		api = self.main.ut.load_yaml(sub_entry.filePath())
		#print api
		## TODO Qtify
		if 'section' in api and api['section']:
			section =  api['section']
		else:
			section = "#"
		#items = self.tree.findItems(section_path, QtCore.Qt.MatchExactly, self.COLS.section)
		#print items, section_path
		#if len(items) == 0:
		#	sectionItem = QtGui.QTreeWidgetItem(parentNode)
		#	sectionItem.setText(self.COLS.icon, api['section'])
		#	sectionItem.setText(self.COLS.section, section_path)
		#items = self.tree.findItems(section_path, QtCore.Qt.MatchExactly, self.COLS.section)
		#print "Second", items, section_path
		#"""
		#else:
		#	print items

		#print api
		funkFileItem = QtGui.QTreeWidgetItem(parentNode)
		funkFileItem.setIcon(self.COLS.icon, Icon(Ico.Function))
		funkFileItem.setText(self.COLS.icon, sub_entry.fileName())
		if 'syntax' in api:
			funkFileItem.setText(self.COLS.icon, api['syntax'])
		funkFileItem.setText(self.COLS.description, api['summary'])
		funkFileItem.setText(self.COLS.function, api['function'])
		funkFileItem.setText(self.COLS.folder, folder)
		funkFileItem.setText(self.COLS.section, section)
		funkFileItem.setData(self.COLS.icon, QtCore.Qt.UserRole, QtCore.QVariant(sub_entry.filePath()))
		#self.tree.setItemExpanded(funkFileItem, True)
		if self.chkExtendedNodes.isChecked():
			if len(api['parameters']) > 0: ##TODO Qt'ify python code
				if 'paramaters_type' in api and 'parameters_type' =='fixed':
					for ap in api['parameters']:
						kidd = QtGui.QTreeWidgetItem(funkFileItem)
						kidd.setIcon(self.COLS.icon, Icon(Ico.Green))
						kidd.setText(self.COLS.icon, ap.keys()[0])
						kidd.setText(self.COLS.description, ap.values()[0])
						kidd.setData(self.COLS.icon, QtCore.Qt.UserRole, QtCore.QVariant(sub_entry.filePath()))
	
			if 'return' in api:
				kidd = QtGui.QTreeWidgetItem(funkFileItem)
				kidd.setIcon(self.COLS.icon, Icon(Ico.Blue)) 
				lbl = QtCore.QString("Return: ").append(api['return'])
				kidd.setText(self.COLS.icon, lbl)
				kidd.setData(self.COLS.icon, QtCore.Qt.UserRole, QtCore.QVariant(sub_entry.filePath()))

	def on_tree_item_clicked(self, item, column):
		is_funk = item.text(self.COLS.function).length() > 0
		self.folderactionGroup.setDisabled(is_funk)
		self.actionAddFunction.setDisabled(False)
		self.actionEditFunction.setDisabled(not is_funk)
		self.actionDeleteFunction.setDisabled(not is_funk)

	def on_tree_item_double_clicked(self, item, column):
		#print item, column
		#print item.text(0), item.data(0, QtCore.Qt.UserRole).toString()
		if item.text(self.COLS.function).length() > 0:
			
			file_path = item.data(self.COLS.icon, QtCore.Qt.UserRole).toString()
			#print "its a function", file_path
			fInfo = QtCore.QFileInfo(file_path)
			dialog = FunctionEditDialog(self, self.main, fInfo.fileName(),  item.text(self.COLS.folder), self.paths)
			self.connect(dialog, QtCore.SIGNAL("refresh"), self.on_refresh)
			res = dialog.exec_()
			if res:
				self.load()