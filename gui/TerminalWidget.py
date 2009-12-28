# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui


from gui.icons import Ico 
from gui.icons import Icon 

class TerminalWidget(QtGui.QWidget):

	
	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self, parent)

		self.main = main
		self.process = QtCore.QProcess(self)
		self.current_file_path = None
		
		layout = QtGui.QVBoxLayout()
		layout.setContentsMargins(0,0,0,0)
		layout.setSpacing(0)
		self.setLayout(layout)

		#self.headerWidget = QtGui.QWidget()
		headLAy = QtGui.QHBoxLayout()
		layout.addLayout(headLAy)

		self.headerLabel = QtGui.QLabel("Terminal Output")
		headLAy.addWidget(self.headerLabel, 10)

		self.progress = QtGui.QProgressBar()
		self.progress.setRange(0,0)
		self.progress.hide()
		headLAy.addWidget(self.progress, 1)

		"""
		toolbar = QtGui.QToolBar()
		toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		layout.addWidget(toolbar)

		toolbar.addAction(Icon(Ico.Compile), "Compile")
		"""

		self.textWidget = QtGui.QPlainTextEdit()
		layout.addWidget(self.textWidget)
		self.textWidget.setDocumentTitle("Foo")
		self.textWidget.setStyleSheet("color: white; background-color: black;")

	def set_text(self, txt, is_error):
		if is_error:
			self.headerLabel.setText("Error")
		else:
			self.headerLabel.setText("result")
		self.textWidget.setPlainText(txt)


	def compile(self, file_path):

		self.current_file_path = file_path
		## Write out enviroment variables to ~/.ardmake.conf
		#ard_make = QtCore.QString()
		env = QtCore.QStringList()
		env << QtCore.QString("ARDUINO_DIR=").append(self.main.settings.arduino_path())
		env << QtCore.QString("ARDUINO_BOARD=").append("atmega328")
		env << QtCore.QString("ARDUINO_sPORT=").append("s/ssdev/ttyUSB0")
		self.process.setEnvironment(env)
		#ard_make.append("ARDUINO_DIR=").append(self.main.settings.arduino_path()).append("\n")
		#ardmake_file_path = QtCore.QDir.homePath().append("/.ardmake.conf")
		# ardmake_file_path
		#self.main.ut.write_file(ardmake_file_path, ard_make)
		print "----------------------------------------"

		sketch_dir = QtCore.QFileInfo(self.current_file_path).absolutePath()
		print "ketch_dir=", sketch_dir, self.current_file_path
		self.process.setWorkingDirectory(sketch_dir)

		command = QtCore.QString("sh ")
		## Create command sh arduinp_make.sh 
		#command.append("pwd  ") #.append(QtCore.QFileInfo(self.current_file_path).dir().path())
		#args = QtCore.QStringList()
		command.append(self.main.settings.app_path()).append("/etc/arduino_make.sh compile ")
		#command.append(QtCore.QFileInfo(self.current_file_path).dir().path())
		print "command=", command
		self.process.start(command)
		if self.process.waitForStarted(): 
			self.process.waitForFinished();
			result =  self.process.readAllStandardOutput()
			#print type(result), result
			error = self.process.readAllStandardError()
			#print type(error), error
			if error:
				print error
				self.textWidget.setPlainText(QtCore.QString(error))
			else:
				self.textWidget.setPlainText(QtCore.QString(result))
		return
		command = QtCore.QString()
		## Create command sh arduinp_make.sh 
		command.append("pwd") # sh ").append(self.main.settings.app_path()).append("/etc/arduino_make.sh compile")
		#args = QtCore.QStringList()
		#command.append(self.main.settings.app_path()).append("/etc/arduino_make.sh compile ")
		#command.append(QtCore.QFileInfo(self.current_file_path).dir().path())
		print "command=", command
		process = QtCore.QProcess(self)
		process.start(command)
		if process.waitForStarted(): 
			process.waitForFinished();
			result =  process.readAllStandardOutput()
			#print type(result), result
			error = process.readAllStandardError()
			#print type(error), error
			if error:
			
				self.textWidget.setPlainText(QtCore.QString(error))
			else:
				self.textWidget.setPlainText(QtCore.QString(result))