# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

import gui.widgets
from gui.icons import Ico 
from gui.icons import Icon 

class SettingsDialog(QtGui.QDialog):

	def __init__(self, parent, main):
		QtGui.QDialog.__init__(self, parent)
		self.main = main

		self.setWindowTitle("Settings")
		self.setWindowIcon(Icon(Ico.Settings))
		self.setMinimumWidth(700)
		self.setMinimumHeight(500)

		mainLayout = QtGui.QVBoxLayout()
		self.setLayout(mainLayout)

		self.path_keys = []
		self.path_keys.append( ['path/arduino_root','Arduino Path', 'Directory of arduino installation'] )
		self.path_keys.append( ['path/sketchbooks_path', 'Sketchbooks',	'Directory to sketchbooks'] )
		self.path_keys.append( ['path/arduino_svn', 'Arduino Svn', 'Path to svn trunk/'] )

		vBox = QtGui.QVBoxLayout()
		vBox.setSpacing(20)
		mainLayout.addLayout(vBox)


		promptButtonGroup = QtGui.QButtonGroup(self)
		self.connect(promptButtonGroup, QtCore.SIGNAL("buttonClicked(QAbstractButton *)"), self.on_prompt_button)

		browseButtonGroup = QtGui.QButtonGroup(self)
		self.connect(browseButtonGroup, QtCore.SIGNAL("buttonClicked(QAbstractButton *)"), self.on_browse_button)

		self.txt = {}
		self.lbl = {}
		#butt = {}
		#buttP = {}
		for fKey, title, description in self.path_keys:

			grp = QtGui.QGroupBox( "%s" % (title) )
			vBox.addWidget(grp)
			vb = QtGui.QVBoxLayout()
			grp.setLayout(vb)
			
			lbl = QtGui.QLabel( description )
			vb.addWidget(lbl)

			pth = self.main.settings.value(fKey)
			self.txt[fKey] = QtGui.QLineEdit(pth) #setval.toString())
			self.txt[fKey].setReadOnly(True)
			vb.addWidget(self.txt[fKey])

			hBox = QtGui.QHBoxLayout()
			vb.addLayout(hBox)

			self.lbl[fKey] = QtGui.QLabel("-")
			hBox.addWidget(self.lbl[fKey])
			self.check_file(fKey)

			buttP = QtGui.QToolButton(self)
			#buttP[fKey].setIcon(dIcon(dIco.Green))
			buttP.setText("Prompt")
			buttP.setProperty("ki", QtCore.QVariant(fKey) )
			buttP.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
			hBox.addWidget(buttP)
			buttP.setVisible(False)
			promptButtonGroup.addButton(buttP)

			buttB = QtGui.QToolButton(self)
			#butt[fKey].setIcon(dIcon(dIco.Green))
			buttB.setText("Browse")
			buttB.setProperty("ki", QtCore.QVariant(fKey) )
			buttB.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
			hBox.addWidget(buttB)
			browseButtonGroup.addButton(buttB)	

		vBox.addStretch(10)

		#########################################
		## Save Cancel Buttons
		buttonBox = QtGui.QHBoxLayout()
		mainLayout.addLayout(buttonBox)
		buttonBox.addStretch(20)

		cancelButton = gui.widgets.CancelButton(self, "Cancel")
		buttonBox.addWidget(cancelButton)

		saveButton = gui.widgets.SaveButton(self)
		buttonBox.addWidget(saveButton)

	def check_file(self, ki):
		file_path = self.txt[ki].text().trimmed()
		if file_path.length() == 0:
			self.lbl[ki].setText("** Not set")
			return

		fileInfo = QtCore.QFileInfo(file_path)
		if not fileInfo.isDir():
			self.lbl[ki].setText("** Not a directory")
			return
		if not fileInfo.exists():
			self.lbl[ki].setText("** Not Exist")
			return
		if fileInfo.isDir():
			self.lbl[ki].setText("Ok - path exists")
			return



	def on_prompt_button(self, butt):
		ki = str(butt.property("ki").toString())
		decoded_text = QtCore.QDir.toNativeSeparators( self.txt[ki].text() )
		txt, ok = QtGui.QInputDialog.getText(self, "Enter path:", " %s path:" % ki, QtGui.QLineEdit.Normal, decoded_text)
		if ok:
			self.set_path_from_raw(ki, txt)

	def on_browse_button(self, butt):
		ki = str(butt.property("ki").toString())
		
		#print "on_dir_select", ki
		fileDialog = QtGui.QFileDialog(self)
		fileDialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
		fileDialog.setMinimumWidth(700)
		fileDialog.setMinimumHeight(700)
		if fileDialog.exec_():		
			#print fileDialog.selectedFiles()[0]
			path = fileDialog.selectedFiles()[0]
			#self.settings.setValue("paths\%s" % ki, QtCore.QVariant( path ) )
			#self.txt[ki].setText( path )
			self.set_path_from_raw(ki, path)


	def set_path_from_raw(self, ki, txt):
		#print "set", ki, txt
		#print self.txt
		new_path = QtCore.QDir.fromNativeSeparators(txt)
		self.emit(QtCore.SIGNAL("pathchanged"), ki, new_path)
		self.txt[ki].setText( new_path)
		self.check_file(ki)

	def set_text(self, ki, va):
		if ki in self.txt:
			self.txt[ki].setText(va) 


	def on_cancel(self):
		self.reject()

	def on_save(self):
		for x in self.path_keys:
			#print x[0], self.txt[x[0]].text()
			self.main.settings.setValue(x[0], self.txt[x[0]].text())
		self.main.settings.qSettings.sync()
		self.emit(QtCore.SIGNAL("refresh_settings"))
		self.accept()
