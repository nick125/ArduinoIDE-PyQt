# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

from gui.icons import Ico 
from gui.icons import Icon 


class ArduinoCompilerBar(QtGui.QWidget):

	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self)

		mainLayout = QtGui.QVBoxLayout()
		self.setLayout(mainLayout)

		### Action Buttons
		commandButtonBarLayout = QtGui.QHBoxLayout()
		mainLayout.addLayout(commandButtonBarLayout)

		buttz = []
		buttz.append(['compile', 'Compile', Ico.Compile])
		buttz.append(['upload', 'Upload', Ico.Upload])
		buttz.append(['compile_upload', 'Compile Upload', Ico.CompileUpload])
		self.buttCompileGroup = QtGui.QButtonGroup()
		self.connect(self.buttCompileGroup, QtCore.SIGNAL("buttonClicked (QAbstractButton *)"), self.on_compile_group_button)
		## TODO connect
		for action_ki, caption, ico in buttz:
			butt = QtGui.QPushButton()
			butt.setProperty('compile_action', action_ki)
			butt.setText(caption)
			butt.setIcon(Icon(ico))
			commandButtonBarLayout.addWidget(butt)
			self.buttCompileGroup.addButton(butt)
		#toolbar.addSeparator()
	
		## Autosave
		groupBox = QtGui.QGroupBox("Autosave")
		mainLayout.addWidget(groupBox)
		groupLayout = QtGui.QVBoxLayout(self)
		groupBox.setLayout(groupLayout)
		self.checkBoxAutoSave = QtGui.QCheckBox(self)
		groupLayout.addWidget(self.checkBoxAutoSave)

		## Board Selection
		groupBox = QtGui.QGroupBox("Board")
		mainLayout.addWidget(groupBox)
		groupLayout = QtGui.QVBoxLayout(self)
		groupBox.setLayout(groupLayout)
		self.comboBoard = QtGui.QComboBox(self)
		groupLayout.addWidget(self.comboBoard)
		## TODO load from app.Boards.index()
		self.comboBoard.addItem("Arduino Dawn")
		self.comboBoard.setCurrentIndex(0)

		## Port Selection
		groupBox = QtGui.QGroupBox("Port")
		mainLayout.addWidget(groupBox)
		groupLayout = QtGui.QVBoxLayout(self)
		groupBox.setLayout(groupLayout)
		self.comboPort = QtGui.QComboBox(self)
		groupLayout.addWidget(self.comboPort)
		## TODO load from app.Ports.index()
		self.comboPort.addItem("/usb/serial/tty/0")
		self.comboPort.setCurrentIndex(0)


		## Serial Sent Selection
		groupBox = QtGui.QGroupBox("Serial Out")
		mainLayout.addWidget(groupBox)
		groupLayout = QtGui.QVBoxLayout()
		groupBox.setLayout(groupLayout)
		self.txtSerialOut = QtGui.QPlainTextEdit(self)
		groupLayout.addWidget(self.txtSerialOut)
		## TODO load from app.Ports.index()
	
		## Serial Sent Selection
		groupBox = QtGui.QGroupBox("Serial In")
		mainLayout.addWidget(groupBox)
		groupLayout = QtGui.QVBoxLayout()
		groupBox.setLayout(groupLayout)
		self.txtSerialIn = QtGui.QPlainTextEdit(self)
		groupLayout.addWidget(self.txtSerialIn)
		## TODO load from app.Ports.index()

	##########################################
	## Compile Upload Buttons
	##########################################	
	def on_compile_group_button(self, butt):
		print "COMP", butt.text(), butt.property("compile_action").toString()
		if butt.text() == "Compile":
			#self.write_file()
			#self.compile_file()
			print "Compile"
		#else:
			#self.main.status.showMessage("Not recognised", 4000)
		compile_action_string = butt.property("compile_action").toString()
		self.emit(QtCore.SIGNAL("compile_action"), compile_action_string)

	#def compile_file(self):
		#self.terminalWidget.compile(self.current_file_path)

	

