# -*- coding: utf-8 -*-

import yaml
from PyQt4 import QtCore, QtGui
import os.path

import app.utils

from app.settings import settings

from gui.FunctionEditDialog import FunctionEditDialog
from gui.icons import Ico, Icon

class APIBrowserPane(QtGui.QWidget):
	"""
		Create the API Browser pane
	"""

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
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)
		self.setLayout(layout)

		###########################
		### Toolbar
		toolbar = QtGui.QToolBar()
		toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		layout.addWidget( toolbar )

		act = toolbar.addAction(Icon(Ico.Refresh), "Refresh", self.on_refresh)
		self.chkExtendedNodes = QtGui.QCheckBox("Show vars")
		self.chkExtendedNodes.setChecked(False)
		toolbar.addWidget(self.chkExtendedNodes)
		self.connect(self.chkExtendedNodes, QtCore.SIGNAL("clicked()"), self.on_refresh)
		toolbar.addSeparator()
		
		#############################################
		### Function Actions
		self.actionAddFunction = toolbar.addAction(Icon(Ico.FunctionAdd), "Add", self.on_add_function)

		self.actionEditFunction = toolbar.addAction(Icon(Ico.FunctionEdit), "Edit", self.on_edit_function)
		self.actionEditFunction.setDisabled(True)

		self.actionDeleteFunction = toolbar.addAction(Icon(Ico.FunctionDelete), "Delete", self.on_delete_function)
		self.actionDeleteFunction.setDisabled(True)
		toolbar.addSeparator()

		#############################################
		### Folder Actions
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

		#############################################
		### Tree
		self.tree = QtGui.QTreeWidget()
		self.tree.setRootIsDecorated(True)
		self.tree.setAlternatingRowColors(True)
		layout.addWidget(self.tree)
		self.connect(self.tree, QtCore.SIGNAL("itemDoubleClicked (QTreeWidgetItem *,int)"), self.on_tree_item_double_clicked)
		self.connect(self.tree, QtCore.SIGNAL("itemClicked (QTreeWidgetItem *,int)"), self.on_tree_item_clicked)

		self.tree.headerItem().setText(self.COLS.icon, "Function")
		self.tree.headerItem().setText(self.COLS.description, "Description")
		self.tree.headerItem().setText(self.COLS.section, "Section")
		self.tree.headerItem().setText(self.COLS.function, "Function")
		self.tree.headerItem().setText(self.COLS.folder, "Folder")
		self.tree.header().setStretchLastSection(True)
		self.tree.setColumnWidth(self.COLS.icon, 300)
		self.tree.setColumnWidth(self.COLS.description, 300)
		if 1 == 0: # ?? umm pedro
			#self.tree.setColumnHidden(self.COLS.folder, True)
			self.tree.setColumnHidden(self.COLS.function, True)
			self.tree.setColumnHidden(self.COLS.folder, True)

		self.api_lines = None
		self.load()

	#####################

	####### This crap walks the Qt Widget to write the file
	#########################
	def on_write_api_file(self):
		rootItem = self.tree.invisibleRootItem()
		self.api_lines = []
		self.extract_api(rootItem)
		for l in self.api_lines:
			print l
		api_string = "\n".join(self.api_lines)
		file_path = settings.def_path().absoluteFilePath("autocomplete.txt")
		app.utils.write_file(file_path, api_string)

	def extract_api(self, treeItem):
		#print "extract"
		if treeItem.childCount() > 0:
			for idx in range(0, treeItem.childCount()):
				item = treeItem.child(idx)
				#print item
				if item.text(self.COLS.function).length() > 0:
					file_path = item.data(self.COLS.icon, QtCore.Qt.UserRole).toString()
					api = app.utils.load_yaml(file_path)
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
			pth = settings.def_path().absoluteFilePath(parent_folder)
			print pth
			dirr = QtCore.QDir(pth)
			success = dirr.mkdir(txt)
			if success:
				self.load()
			else:
				print "error" # TODO

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
		root_path = settings.api_define_path()
		rootDir = QtCore.QDir(root_path)
		self.paths = []
		self.walk_dir(rootDir, '', rootNode)

	def walk_dir(self, sub_dir, folder, parentItem):
	
		for file_entry in sub_dir.entryInfoList(QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot):
			if file_entry.suffix() == 'yaml':
				self.add_yaml_function_node(file_entry, folder, parentItem)
	
		for folder_entry in sub_dir.entryInfoList(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot):
			n_folder =  folder+ folder_entry.fileName() + '/'
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
		api = app.utils.load_yaml(sub_entry.filePath())
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
		is_fixed = 'parameters_type' in api and api['parameters_type'] == 'fixed'
		if not is_fixed:
			#print "foo"
			s = api['function'] + "(*)"
			funkFileItem = QtGui.QTreeWidgetItem(parentNode)
			funkFileItem.setIcon(self.COLS.icon, Icon(Ico.Function))
			funkFileItem.setData(self.COLS.icon, QtCore.Qt.UserRole, sub_entry.fileName())
			funkFileItem.setText(self.COLS.folder, folder)
			font = funkFileItem.font(self.COLS.icon)
			font.setBold(True)
			funkFileItem.setFont(self.COLS.icon, font)
			funkFileItem.setText(self.COLS.icon, s)
			funkFileItem.setText(self.COLS.function, api['function'])
			
			if len(api['parameters']) > 0:
				#p_list = []
				for ap in api['parameters']:
					paraSyntax = QtGui.QTreeWidgetItem(funkFileItem)
					paraSyntax.setIcon(self.COLS.icon, Icon(Ico.FunctionSub))
					paraSyntax.setData(self.COLS.icon, QtCore.Qt.UserRole, sub_entry.fileName())
					font = funkFileItem.font(self.COLS.icon)
					font.setBold(True)
					paraSyntax.setFont(self.COLS.icon, font)

					#sss  = "<font color=blue><b>%s</b></font>" % ap.keys()[0]
					#sss = ap.keys()[0]
					#p_list.append(sss)
				#s += "( " + ", ".join(p_list)+ " )"
				#kidd = QtGui.QTreeWidgetItem(funkFileItem)
				#kidd.setIcon(self.COLS.icon, Icon(Ico.Green))
			#else:
				#s += "()"
			#s += " - <small>%s</small>" % api['summary']
					func_name = api['function']
					#if api['function'].find(".") > 1:
						#self.api_lines.append(api['function'] + "()")
						#func_name = "." + api['function'].split(".")[1]
					if ap.keys()[0] == '':
						s = func_name + "()"
					else:
						s = func_name + "( " + ap.keys()[0] + " )"
					paraSyntax.setText(self.COLS.icon, s)
					paraSyntax.setText(self.COLS.description, ap.values()[0])
					paraSyntax.setText(self.COLS.function, api['function'])
					paraSyntax.setText(self.COLS.folder, folder)

		else:
			funkFileItem = QtGui.QTreeWidgetItem(parentNode)
			funkFileItem.setIcon(self.COLS.icon, Icon(Ico.Function))
			#funkFileItem.setText(self.COLS.icon, sub_entry.fileName())
			font = funkFileItem.font(self.COLS.icon)
			font.setBold(True)
			funkFileItem.setFont(self.COLS.icon, font)
			#if 'syntax' in api:
			#	funkFileItem.setText(self.COLS.icon, api['syntax'])
			ss = "<b><font color=#176087 >%s</font></b>" % api['function']
			s = api['function']
			if len(api['parameters']) > 0:
				p_list = []
				for ap in api['parameters']:
					#sss  = "<font color=blue><b>%s</b></font>" % ap.keys()[0]
					sss = ap.keys()[0]
					p_list.append(sss)
				s += "( " + ", ".join(p_list)+ " )"
				#kidd = QtGui.QTreeWidgetItem(funkFileItem)
				#kidd.setIcon(self.COLS.icon, Icon(Ico.Green))
			else:
				s += "()"
			#s += " - <small>%s</small>" % api['summary']
			funkFileItem.setText(self.COLS.icon, s)
			#lbl = QtGui.QLabel(s, self.tree)
			#lbl.setAutoFillBackground(True)
			#self.tree.setItemWidget(funkFileItem, self.COLS.icon, lbl)
			#kidd.setText(self.COLS.description, ap.values()[0])
			#kidd.setData(self.COLS.icon, QtCore.Qt.UserRole, QtCore.QVariant(sub_entry.filePath()))

			funkFileItem.setText(self.COLS.description, api['summary'])
			funkFileItem.setText(self.COLS.function, api['function'])
			funkFileItem.setText(self.COLS.folder, folder)
			#funkFileItem.setText(self.COLS.section, section)
			funkFileItem.setData(self.COLS.icon, QtCore.Qt.UserRole, QtCore.QVariant(sub_entry.filePath()))
			#self.tree.setItemExpanded(funkFileItem, True)
			#print  api['parameters']
			if  self.chkExtendedNodes.isChecked():
				if len(api['parameters']) > 0: ##TODO Qt'ify python code
					if 'parameters_type' in api and api['parameters_type'] =='fixed':
						
						for ap in api['parameters']:
							kidd = QtGui.QTreeWidgetItem(funkFileItem)
							kidd.setIcon(self.COLS.icon, Icon(Ico.FunctionParam))
							kidd.setText(self.COLS.icon, ap.keys()[0])
							kidd.setText(self.COLS.description, ap.values()[0])
							kidd.setData(self.COLS.icon, QtCore.Qt.UserRole, QtCore.QVariant(sub_entry.filePath()))
		
				if 'return' in api and api['return'] != '':
					kidd = QtGui.QTreeWidgetItem(funkFileItem)
					kidd.setIcon(self.COLS.icon, Icon(Ico.FunctionReturn)) 
					lbl = QtCore.QString("Return: ").append(api['return'])
					kidd.setText(self.COLS.icon, lbl)
					kidd.setData(self.COLS.icon, QtCore.Qt.UserRole, QtCore.QVariant(sub_entry.filePath()))
					kidd.setFirstColumnSpanned(True)

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
