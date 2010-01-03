# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

import app.Boards
import app.SerialPorts

from gui.icons import Ico 
from gui.icons import Icon 


class ArduinoCompilerBar(QtGui.QWidget):

	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self)

		self.project_settings = None

		## Main Vertical Layout
		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setContentsMargins(0,0,0,0)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)

		##############################################################
		### Compile/Command Buttons Bar
		commandButtonBarLayout = QtGui.QHBoxLayout()
		commandButtonBarLayout.setContentsMargins(0,0,0,0)
		commandButtonBarLayout.setSpacing(0)
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
	
		########################################################
		## Tree's Toolbar
		########################################################
		toolbar = QtGui.QToolBar()
		mainLayout.addWidget(toolbar)
		toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

		##########################################
		## Select Board Button and menu
		tbSelectBoardButton = QtGui.QToolButton()
		tbSelectBoardButton.setText("Select Board")
		tbSelectBoardButton.setPopupMode(QtGui.QToolButton.InstantPopup)
		toolbar.addWidget(tbSelectBoardButton)
		
		self.actionBoardsGroup = QtGui.QActionGroup(self)
		self.connect(self.actionBoardsGroup, QtCore.SIGNAL("triggered(QAction *)"), self.on_action_select_board)
		self.actionBoardsGroup.setExclusive(True)
		self.menuSelectBoard = QtGui.QMenu(tbSelectBoardButton)
		tbSelectBoardButton.setMenu(self.menuSelectBoard)

		######################################
		## Select Port Button and menu
		tbSelectPortButton = QtGui.QToolButton()
		tbSelectPortButton.setText("Select Port")
		tbSelectPortButton.setPopupMode(QtGui.QToolButton.InstantPopup)
		toolbar.addWidget(tbSelectPortButton)
		
		self.actionPortsGroup = QtGui.QActionGroup(self)
		self.connect(self.actionPortsGroup, QtCore.SIGNAL("triggered(QAction *)"), self.on_action_select_port)
		self.menuSelectPort = QtGui.QMenu(tbSelectBoardButton)
		tbSelectPortButton.setMenu(self.menuSelectPort)

		
		############################################################
		## Tree - third column is the key value [autosave, boards, port]
		###########################################################
		self.treeInfo = QtGui.QTreeWidget(self)
		mainLayout.addWidget(self.treeInfo)
		self.treeInfo.header().hide()
		self.treeInfo.setAlternatingRowColors(True)
		self.treeInfo.setRootIsDecorated(False)
		self.treeInfo.setColumnCount(3) ## Third column is the "ki"
		self.treeInfo.setFixedHeight(80) ## hack
		self.treeInfo.setColumnHidden(2, True) # hacking
		
		item = QtGui.QTreeWidgetItem()
		item.setText(0, 'AutoSave')
		item.setText(1, 'Off')
		item.setCheckState(1, QtCore.Qt.Unchecked)
		item.setText(2, "autosave")
		self.treeInfo.addTopLevelItem(item)

		item = QtGui.QTreeWidgetItem()
		item.setText(0, 'Board')
		item.setText(1, '-- None --')
		item.setIcon(0, Icon(Ico.Board))
		item.setText(2, "board")
		self.treeInfo.addTopLevelItem(item)

		item = QtGui.QTreeWidgetItem()
		item.setText(0, 'Serial Port')
		item.setText(1, '-- None --')
		item.setIcon(0, Icon(Ico.SerialPort))
		item.setText(2, "serial_port")
		self.treeInfo.addTopLevelItem(item)


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


		self.load_boards()
		self.load_serial_ports()
		#self.set_buttons_status()



	##########################################
	## Compile Upload Buttons
	##########################################	
	def on_compile_group_button(self, butt):
		#print "COMP", butt.text(), butt.property("compile_action").toString()
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

	def set_compile_buttons_status(self):
		return
		disabled = True if self.selected_board == None or self.selected_serial_port == None else False 
		for butt in self.buttCompileGroup.buttons():
			butt.setDisabled(disabled)

	
	##########################################
	## Board Related
	##########################################	
	def load_boards(self):
		boardsObj = app.Boards.Boards(self)
		for board, name in boardsObj.index():
			act = QtGui.QAction(self)
			act.setText(name)
			act.setProperty("board", board)
			act.setCheckable(True)
			self.actionBoardsGroup.addAction(act)
			self.menuSelectBoard.addAction(act)

	def on_action_select_board(self, act):
		if not 'board' in self.project_settings:
			self.project_settings['board'] = {}

		self.project_settings['board'] = {'board': str(act.property("board").toString()),
										'name': str(act.text()) }
		items = self.treeInfo.findItems("board", QtCore.Qt.MatchExactly, 2)
		items[0].setText(1, self.project_settings['board']['name'])
		self.set_compile_buttons_status()
		self.emit(QtCore.SIGNAL('project_settings_changed'), self.project_settings)
			
	##########################################
	## Serial Port Related
	##########################################	
	def load_serial_ports(self):
		#self.selected_serial_port = None
		portsObj = app.SerialPorts.SerialPorts(self)
		for serial_port in portsObj.index():
			act = QtGui.QAction(self)
			act.setText(serial_port)
			act.setProperty("serial_port", serial_port)
			act.setCheckable(True)
			self.actionPortsGroup.addAction(act)
			self.menuSelectPort.addAction(act)
		

	def on_action_select_port(self, act):
		self.project_settings['serial_port'] = {'serial_port': str(act.property("serial_port").toString())}
		items = self.treeInfo.findItems("serial_port", QtCore.Qt.MatchExactly, 2)
		items[0].setText(1, self.project_settings['serial_port']['serial_port'])
		self.set_compile_buttons_status()
		self.emit(QtCore.SIGNAL('project_settings_changed'), self.project_settings)



	def set_project(self, project_settings):
		self.project_settings = project_settings
		if self.project_settings == None:
			self.project_settings = {}
			return
		if 'board' in self.project_settings:
			items = self.treeInfo.findItems("board", QtCore.Qt.MatchExactly, 2)
			items[0].setText(1, self.project_settings['board']['name'])

		if 'serial_port' in self.project_settings:
			items = self.treeInfo.findItems("serial_port", QtCore.Qt.MatchExactly, 2)
			items[0].setText(1, self.project_settings['serial_port']['serial_port'])
