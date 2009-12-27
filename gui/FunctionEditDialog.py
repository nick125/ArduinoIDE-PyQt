# -*- coding: utf-8 -*-

import yaml
from yaml import Loader, Dumper
from PyQt4 import QtCore, QtGui

import gui.widgets
from gui.icons import Ico 
from gui.icons import Icon 

class FunctionEditDialog(QtGui.QDialog):
	
	def __init__(self, parent, main, function_file=None):
		QtGui.QDialog.__init__(self, parent)

		self.main = main
		self.function_file = function_file

		mainLayout = QtGui.QVBoxLayout()
		self.setLayout(mainLayout)


		gridLayout = QtGui.QGridLayout()
		mainLayout.addLayout(gridLayout)
		row = 0

		## Function
		gridLayout.addWidget(QtGui.QLabel("Function:"), row, 0, QtCore.Qt.AlignRight)
		self.txtFunction = QtGui.QLineEdit()
		gridLayout.addWidget(self.txtFunction, row, 1)
		gridLayout.addWidget(QtGui.QLabel("Name eg digitialFilter()"), row, 2)


		## Lib
		row  += 1
		gridLayout.addWidget(QtGui.QLabel("Lib:"), row, 0, QtCore.Qt.AlignRight)
		self.txtLib = QtGui.QLineEdit()
		#self.cmbLib.addItem("arduino")
		#self.cmbLib.addItem("servo")
		#self.cmbLib.addItem("stepper")
		gridLayout.addWidget(self.txtLib, row, 1)
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
		gridLayout.addWidget(self.txtSyntax, row, 1)
		gridLayout.addWidget(QtGui.QLabel("eg digitalWrite(pin, value)"), row, 2)

		## Tooltip
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
		cancelButton = gui.widgets.CancelButton(self, "Cancel")
		bbox.addWidget(cancelButton, 1)
		self.saveButton = gui.widgets.SaveButton(self)
		bbox.addWidget(self.saveButton, 1)

		if self.function_file:
			self.load_file()

	def on_cancel(self):
		pass

	def on_save(self):
		self.txtFunction.setText(self.txtFunction.text().trimmed())
		if not self.txtFunction.text().endsWith("()"):
			self.txtFunction.setFocus()
			return
		funct_name = self.txtFunction.text().mid(0, self.txtFunction.text().length() - 2)
		if funct_name.length() == 0:
			self.txtFunction.setFocus()
			return
		self.function_file = funct_name
		self.save_file()

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
	def load_file(self, file_name=None):

		#file_name = self.main.settings.def_path().append("/digitalWrite.yaml")

		string = self.main.ut.get_file_contents(self.function_file)
		#print string

		data = yaml.load(str(string))
		self.txtFunction.setText(data['function'])
		self.txtLib.setText(data['lib'])
		self.txtSection.setText(data['section'])
		self.txtSyntax.setText(data['syntax'])
		self.txtSummary.setText(data['summary'])

		#self.txtParameters.setPlainText(data['parameters'])
		self.txtDescription.setPlainText(data['description'])
		self.txtExample.setPlainText(data['example'])


		print "all=", data['parameters']
		for dic in data['parameters']:
			#print ki #ki, data['parameters'][ki]
			print dic.keys(), dic.values()
			treeItem = QtGui.QTreeWidgetItem()
			treeItem.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			treeItem.setText(0, dic.keys()[0])
			treeItem.setText(1, dic.values()[0])
			self.tree.addTopLevelItem(treeItem)

	#############################################
	## Save
	#############################################
	def save_file(self):
		dic = {}
		dic['function'] = str(self.txtFunction.text())
		dic['lib'] = str(self.txtLib.text())
		dic['section'] = str(self.txtSection.text())
		dic['syntax'] = str(self.txtSyntax.text())
		dic['summary'] = str(self.txtSummary.text())
		dic['description'] = str(self.txtDescription.toPlainText())
		dic['example'] = str(self.txtExample.toPlainText())
		dic['parameters'] = []
		rootItem = self.tree.invisibleRootItem()
		for idx in range(0, rootItem.childCount()):
			kid = rootItem.child(idx)
			dic['parameters'].append(  { str(kid.text(0)) : str(kid.text(1))} )


		string = yaml.dump(dic, Dumper=Dumper, default_flow_style=False)
		
		
		#print self.function_name
		#file_path = self.main.settings.def_path().append("/").append(self.function_name).append(".yaml")
		#print file_path
		self.main.ut.write_file(self.function_file, string)
		

