# -*- coding: utf-8 -*-

from operator import itemgetter
from PyQt4 import QtCore, QtGui
from gui.icons import Icon, Ico
from settings import settings

import app.utils

class API(QtCore.QObject):

	def __init__(self):
		QtCore.QObject.__init__(self)

		self.html_files = None 
		self.yaml_files = None

		self.tree = None
		self.functions = None

		self.load_api()

	def load_api(self):
		self.tree = {}
		self.functions = []
		root_path = settings.api_define_path()
		rootDir = QtCore.QDir(root_path)
		self.tree = {}
		self.walk_dir(rootDir, '/')
		#print self.functions

	def walk_dir(self, sub_dir, folder):
	
		if not folder in self.tree:
			self.tree['folder'] = {}
		for file_entry in sub_dir.entryInfoList(QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot):
			if file_entry.suffix() == 'yaml':
				self.functions.append([str(file_entry.completeBaseName()), str(file_entry.filePath())])
	
		for folder_entry in sub_dir.entryInfoList(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot):
			n_folder = folder + folder_entry.fileName() + "/"


			self.walk_dir(QtCore.QDir(folder_entry.filePath()), n_folder)
		
	def add_yaml_function_node(self, sub_entry, folder, parentNode):
		api = app.utils.load_yaml(sub_entry.filePath())
		#print api
		## TODO Qtify
		if 'section' in api and api['section']:
			section =  api['section']
		else:
			section = "#"

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

				
					func_name = api['function']

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
			if  1 == 0:
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















	def tree(self):
		api_path = settings.api_define_path()

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
		
	### Return a list of the html files which is a single dir listing and files ending with .html
	def html_index(self):
		self.html_files = {}
		pathStr = settings.help_path()
		htmlDir = QtCore.QDir(pathStr)
		if not htmlDir.exists():
			#QtGui.QMessageBox.information(self, "OOps", " the reference dir %s was not found" % pathStr)
			print "error", # TODO
			return
		## TODO sort
		for file_entry in htmlDir.entryInfoList(QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot):
			if file_entry.suffix() == 'html':
				self.html_files[str(file_entry.filePath())] = str(file_entry.baseName())

		return self.html_files
