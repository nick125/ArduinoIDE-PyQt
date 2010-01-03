# -*- coding: utf-8 -*-
from PyQt4 import QtCore

from app.settings import settings

class Compiler(QtCore.QObject):

	def __init__(self, parent): #, board=None, port=None, compile_path=None, file_to_compile=None ):
		QtCore.QObject.__init__(self, parent)


	
    #### Then below is the arudino_make.sh ? not yet abstractoed

		
	def ard_make(self, file_to_compile, board, port):
		
		self.file_to_compile = file_to_compile
		self.board = board
		self.port = port
		self.emit(QtCore.SIGNAL("compile_log"), "start_compile", "%s" % self.file_to_compile)
		process = QtCore.QProcess(self)

		arduino_path = settings.arduino_path()
		if not arduino_path:
			self.set_error("Arduino root path not found", "..nothing to do ..")
			#TOD self.emit(
			return
		#print arduino_path.path()
		## ENV - Set Envoironment variables
		env = QtCore.QStringList()
		env << QtCore.QString("ARDUINO_DIR=").append(arduino_path.path())
		env << QtCore.QString("ARDUINO_BOARD=").append(board)
		env << QtCore.QString("ARDUINO_sPORT=").append(port)
		process.setEnvironment(env)
		self.emit(QtCore.SIGNAL("compile_log"), "env", env.join(" "))
		#print "----------------------------------------"

		## Set "process path" to working dir Project Directory
		project_dir = QtCore.QFileInfo(self.file_to_compile).absolutePath()
		process.setWorkingDirectory(project_dir)
		self.emit(QtCore.SIGNAL("compile_log"), "env", "cwd=" % project_dir)

		## construct the command "sh /app_path/etc/arduino_make.sh compile" and execute in project_dir dir
		command = QtCore.QString("sh ")
		#args = QtCore.QStringList()
		script_full_path = settings.app_path().absoluteFilePath("etc/arduino_make.sh compile ")
		command.append(script_full_path)
		#print "command=", command
		self.emit(QtCore.SIGNAL("compile_log"), "command", QtCore.QString(command))
		## Execute process
		process.start(command)
		if process.waitForStarted(): 
			process.waitForFinished()
			result =  process.readAllStandardOutput()
			#print type(result), result
			error = process.readAllStandardError()
			#print type(error), error
			if error:
				#print "is error", error
				#self.actionIcon.setIcon(Icon(Ico.CompileError))
				#self.statusLabel.setText("Error")
				#self.textWidget.setPlainText(QtCore.QString(error))
				#self.emit(QtCore.SIGNAL("compile_error"), QtCore.QString(error))
				self.emit(QtCore.SIGNAL("compile_log"), "error", QtCore.QString(error))
			else:
				#print "is ok", result
				#self.emit(QtCore.SIGNAL("compile_result"), QtCore.QString(result))
				self.emit(QtCore.SIGNAL("compile_log"), "result", QtCore.QString(result))

				#self.statusLabel.setText("OK")
				#self.actionIcon.setIcon(Icon(Ico.CompileOk))
				#self.textWidget.setPlainText(QtCore.QString(result))


		### >>>> DEAD
		#self.progress.hide()
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
