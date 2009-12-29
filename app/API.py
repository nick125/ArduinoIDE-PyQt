# -*- coding: utf-8 -*-

from operator import itemgetter
from PyQt4 import QtCore

class API(QtCore.QObject):

	def __init__(self, main):
		QtCore.QObject.__init__(self, main)

		self.main = main

		self.html_files = None

	def html_index(self):
		self.html_files = {}
		pathStr = self.main.settings.help_path()
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

	def tree(self):
		api_path = self.main.settings.api_define_path()

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
		

