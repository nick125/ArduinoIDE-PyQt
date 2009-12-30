# -*- coding: utf-8 -*-

import yaml
from yaml import Loader, Dumper
from PyQt4 import QtCore, QtGui

import app.utils 

from app.settings import settings

from gui.widgets import GenericWidgets
from gui.icons import Ico 
from gui.icons import Icon 

class FunctionEditDialog(QtGui.QDialog):
	
	def __init__(self, parent, main, function_file, path, paths):
		QtGui.QDialog.__init__(self, parent)

		self.main = main
		self.function_file = function_file
		self.path = path
		self.paths = paths
		self.dic = None
		#print function_file, path, paths

		self.setMinimumWidth(1100)
		self.setMinimumHeight(800)

		mainLayout = QtGui.QVBoxLayout()
		self.setLayout(mainLayout)


		gridLayout = QtGui.QGridLayout()
		mainLayout.addLayout(gridLayout)
		row = 0

		## Function
		gridLayout.addWidget(QtGui.QLabel("Function:"), row, 0, QtCore.Qt.AlignRight)
		self.txtFunction = QtGui.QLineEdit()
		gridLayout.addWidget(self.txtFunction, row, 1)
		gridLayout.addWidget(QtGui.QLabel("Name eg digitialFilter (no brackets)"), row, 2)
		self.connect(self.txtFunction, QtCore.SIGNAL("textChanged(const QString&)"), self.on_function_text_changed)


		## Lib
		row  += 1
		gridLayout.addWidget(QtGui.QLabel("Lib:"), row, 0, QtCore.Qt.AlignRight)
		self.comboLib = QtGui.QComboBox()
		for pth in paths:
			newIdx = self.comboLib.count()
			self.comboLib.insertItem(newIdx, pth)
			print pth, self.path
			if pth == self.path:
				self.comboLib.setCurrentIndex(newIdx)
		gridLayout.addWidget(self.comboLib, row, 1)
		gridLayout.addWidget(QtGui.QLabel("Lib eg arduino"), row, 2)


		## Section
		row  += 1
		gridLayout.addWidget(QtGui.QLabel("Section:"), row, 0, QtCore.Qt.AlignRight)
		self.txtSection = QtGui.QLineEdit()
		gridLayout.addWidget(self.txtSection, row, 1)
		gridLayout.addWidget(QtGui.QLabel("Nav section eg math or digtital IO"), row, 2)


		## Syntax
		row  += 1
		gridLayout.addWidget(QtGui.QLabel("Syntax:"), row, 0, QtCore.Qt.AlignRight)
		self.txtSyntax = QtGui.QLineEdit()
		self.txtSyntax.setReadOnly(True)
		gridLayout.addWidget(self.txtSyntax, row, 1)
		gridLayout.addWidget(QtGui.QLabel(""), row, 2)

		## Summary
		row  += 1
		gridLayout.addWidget(QtGui.QLabel("Summary:"), row, 0, QtCore.Qt.AlignRight)
		self.txtSummary = QtGui.QLineEdit()
		gridLayout.addWidget(self.txtSummary, row, 1)
		gridLayout.addWidget(QtGui.QLabel("Brief popup description"), row, 2)

		## Parameters Widgets tree
		row  += 1
		grpBox = QtGui.QGroupBox("Parameters")
		gridLayout.addWidget(grpBox, row, 0, 1, 3)
		grpLayout = QtGui.QVBoxLayout()
		grpLayout.setSpacing(0)
		grpBox.setLayout(grpLayout)

		toolbar = QtGui.QToolBar()
		toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		grpLayout.addWidget(toolbar)


		self.radioFixed = QtGui.QRadioButton("Fixed params", self)
		toolbar.addWidget(self.radioFixed)
		self.radioVariable = QtGui.QRadioButton("Variable params", self)
		toolbar.addWidget(self.radioVariable)
		toolbar.addSeparator()

		toolbar.addAction(Icon(Ico.Add), "Add", self.on_add_parameter)
		toolbar.addAction(Icon(Ico.Remove), "Remove", self.on_remove_parameter)
		toolbar.addSeparator()
		toolbar.addAction(Icon(Ico.Up), "Up", self.on_move_up)
		toolbar.addAction(Icon(Ico.Down), "Down", self.on_move_down)

		self.tree = QtGui.QTreeWidget()
		self.tree.setRootIsDecorated(False)
		self.tree.headerItem().setText(0, "Parameter")
		self.tree.headerItem().setText(1, "Description")
		grpLayout.addWidget(self.tree)
		self.connect(self.tree, QtCore.SIGNAL("itemChanged(QTreeWidgetItem *,int)"), self.on_tree_changed)

		## Returns
		row  += 1
		self.chkReturn = QtGui.QCheckBox("Return")
		self.connect(self.chkReturn, QtCore.SIGNAL("toggled(bool)"), self.on_chk_return)
		gridLayout.addWidget(self.chkReturn, row, 0, QtCore.Qt.AlignRight)
		self.txtReturn = QtGui.QLineEdit()
		gridLayout.addWidget(self.txtReturn, row, 1, 1, 2)
		#gridLayout.addWidget(QtGui.QLabel("eg milliseconds elapsed"), row, 2)

		## Description
		row  += 1
		grpBox = QtGui.QGroupBox("Description")
		gridLayout.addWidget(grpBox, row, 0, 1, 3)
		grpLayout = QtGui.QVBoxLayout()
		grpBox.setLayout(grpLayout)
		self.txtDescription = QtGui.QPlainTextEdit()
		grpLayout.addWidget(self.txtDescription)

		## Example
		#row  += 1
		grpBox = QtGui.QGroupBox("Example")
		gridLayout.addWidget(grpBox, 0, 3, 7, 1)
		grpLayout = QtGui.QVBoxLayout()
		grpBox.setLayout(grpLayout)
		self.txtExample = QtGui.QPlainTextEdit()
		grpLayout.addWidget(self.txtExample)

		gridLayout.setColumnStretch(0, 0)
		gridLayout.setColumnStretch(1, 2)
		gridLayout.setColumnStretch(2, 0)
		gridLayout.setColumnStretch(3, 3)

		############################################
		## Bottom Buttons
		bbox = QtGui.QHBoxLayout()
		mainLayout.addLayout(bbox)
		bbox.addStretch(20)
		cancelButton = GenericWidgets.CancelButton(self, "Cancel")
		bbox.addWidget(cancelButton, 1)
		self.saveButton = GenericWidgets.SaveButton(self)
		bbox.addWidget(self.saveButton, 1)

		self.statusBar = QtGui.QStatusBar(self)
		mainLayout.addWidget(self.statusBar)

		if self.function_file:
			self.load_file()

	def on_chk_return(self):
		self.txtReturn.setEnabled( self.chkReturn.isChecked() )
		if self.chkReturn.isChecked():
			self.txtReturn.setText( self.dic['return'] )
			self.txtReturn.setFocus()
		else:
			self.txtReturn.setText( '' )
			

	def on_cancel(self):
		self.reject()

	def on_tree_changed(self, item, col):
		self.set_syntax_string()

	def on_add_parameter(self):
		treeItem = QtGui.QTreeWidgetItem(self.tree)
		treeItem.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
		treeItem.setText(0, "-")
		treeItem.setText(1, "--")
		self.tree.addTopLevelItem(treeItem)
		self.tree.setCurrentItem(treeItem)
		self.tree.editItem(treeItem, 0)

	def on_remove_parameter(self):
		item = self.tree.currentItem()
		if not item:
			return
		self.tree.invisibleRootItem().removeChild(item)

	def on_move_up(self):
		pass

	def on_move_down(self):
		pass

	#############################################
	## Load
	#############################################
	def load_file(self):
		_path = settings.api_define_path()
		_path.cd(self.path)
		file_path= _path.absoluteFilePath(self.function_file)
		#print file_path
		string = app.utils.get_file_contents(file_path)
		#print string
		#print "LOAD", file_name
		data = yaml.load(str(string))
		self.dic = data

		self.txtFunction.setText(data['function'])
		#self.txtLib.setText(data['lib'])
		self.txtSection.setText(data['section'])
		self.txtSyntax.setText(data['syntax'])
		self.txtSummary.setText(data['summary'])
		if 'return' in data:
			if data['return'] != '':
				self.txtReturn.setText(data['return'])
				self.txtReturn.setEnabled(True)
				self.chkReturn.setChecked(True)
			else:
				self.txtReturn.setText("")
				self.txtReturn.setEnabled(False)
				self.chkReturn.setChecked(False)
		if 'parameters_type' in data and data['parameters_type'] == 'variable':
			self.radioVariable.setChecked(True)
		else:
			self.radioFixed.setChecked(True)
		self.txtDescription.setPlainText(data['description'])
		self.txtExample.setPlainText(data['example'])


		#print "all=", data['parameters']
		for dic in data['parameters']:
			#print ki #ki, data['parameters'][ki]
			#print dic.keys(), dic.values()
			treeItem = QtGui.QTreeWidgetItem()
			treeItem.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			treeItem.setText(0, dic.keys()[0])
			treeItem.setText(1, dic.values()[0])
			self.tree.addTopLevelItem(treeItem)
		self.set_syntax_string()

	#############################################
	## Save
	#############################################
	def on_save(self): 
		"""Validate the form"""
		self.txtFunction.setText(self.txtFunction.text().trimmed())
		if self.txtFunction.text().indexOf("(") > 0 or self.txtFunction.text().indexOf("(") > 0:
			self.txtFunction.setFocus()
			self.statusBar.showMessage("Function must not contain ( or ) ", 5000)
			return
		#funct_name = self.txtFunction.text().mid(0, self.txtFunction.text().length() - 2)
		if self.txtFunction.text().length() == 0:
			self.txtFunction.setFocus()
			self.statusBar.showMessage("Need a function name", 5000)
			return
		#self.function_file = funct_name
		self.save_file()
		self.emit(QtCore.SIGNAL("refresh"))
		self.accept()

	def save_file(self):
		dic = {}
		dic['function'] = str(self.txtFunction.text())
		dic['folder'] = str(self.comboLib.currentText())
		dic['section'] = str(self.txtSection.text())
		dic['syntax'] = str(self.txtSyntax.text())
		dic['summary'] = str(self.txtSummary.text())
		dic['return'] = str(self.txtReturn.text())
		dic['description'] = str(self.txtDescription.toPlainText())
		dic['example'] = str(self.txtExample.toPlainText())
		dic['parameters_type'] = 'fixed' if self.radioFixed.isChecked() else 'variable'
		dic['parameters'] = []
		print dic['parameters_type']
		rootItem = self.tree.invisibleRootItem()
		for idx in range(0, rootItem.childCount()):
			kid = rootItem.child(idx)
			dic['parameters'].append(  { str(kid.text(0)) : str(kid.text(1))} )


		string = yaml.dump(dic, Dumper=Dumper, default_flow_style=False)
		
		path = self.comboLib.currentText()
		#file_to_save = self.main.settings.def_path().append(path).append(self.function_file)

		
		file_to_save = self.txtFunction.text().trimmed().append(".yaml")
		file_path_to_save = self.main.settings.def_path().append(path).append(file_to_save)

		if self.function_file: # original existed
			original_file_path = self.main.settings.def_path().append(self.path).append(self.function_file)
			#print "=================================+++"
			#print file_path_to_save
			#print original_file_path
			if file_path_to_save != original_file_path:
				QtCore.QFile.remove(original_file_path)
		
		app.utils.write_file(file_path_to_save, string)
		

	def on_function_text_changed(self, string):
		self.set_syntax_string()

	def set_syntax_string(self):
		#print "ere"
		rootItem = self.tree.invisibleRootItem()
		s = self.txtFunction.text()
		if rootItem.childCount() == 0:
			s.append("()")
		else:
			s.append("(")
			params = []
			for idx in range(0, rootItem.childCount()):
				#s.append( self, rootItem.child(idx).text(0) )
				params.append(str(rootItem.child(idx).text(0)))
			s.append(", ".join(params))
			s.append(")")
		self.txtSyntax.setText( s )
