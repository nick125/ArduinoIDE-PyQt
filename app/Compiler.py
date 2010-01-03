# -*- coding: utf-8 -*-
from PyQt4 import QtCore

from app.settings import settings

class Compiler(QtCore.QObject):

	def __init__(self, parent): #, board=None, port=None, compile_path=None, file_to_compile=None ):
		QtCore.QObject.__init__(self, parent)

		self.board = None
		self.serial_port = None


	################################################
	## Make from Project dict
    ################################################
	def arduino_make_project(self, project_settings):
		self.set_project(project_settings)
		self.run_arduino_make()

	def arduino_upload_project(self, project_settings):
		self.set_project(project_settings)
		self.run_arduino_upload()

	## copies dict to class
	def set_project(self, project_settings):
		self.file_to_compile = project_settings['file_path']
		self.project_dir = QtCore.QFileInfo(self.file_to_compile).absolutePath()

		self.board = project_settings['board']['board']
		self.serial_port = project_settings['serial_port']['serial_port']

	## Sets up the Enviroment and working path
	def set_process_env(self, process):
		arduino_path = settings.arduino_path()
		if not arduino_path:
			self.emit(QtCore.SIGNAL("compile_log"), "error","Arduino root path not found")
			#TOD self.emit(
			return False
		env = QtCore.QStringList()
		env << QtCore.QString("ARDUINO_DIR=").append(arduino_path.path())
		env << QtCore.QString("ARDUINO_BOARD=").append(self.board)
		env << QtCore.QString("ARDUINO_PORT=").append(self.serial_port)
		process.setEnvironment(env)
		self.emit(QtCore.SIGNAL("compile_log"), "env", env.join(" "))

		process.setWorkingDirectory(self.project_dir)
		self.emit(QtCore.SIGNAL("compile_log"), "env", "cwd=" % self.project_dir)
		return True

	def run_arduino_make(self):
		self.emit(QtCore.SIGNAL("compile_log"), "start_compile", "%s" % self.file_to_compile)

		process = QtCore.QProcess(self)
		self.set_process_env(process)

		## construct the command "sh /app_path/etc/arduino_make.sh compile" and execute in project_dir dir
		command = QtCore.QString("sh ")
		script_full_path = settings.app_path().absoluteFilePath("etc/arduino_make.sh compile")
		command.append(script_full_path)
		#print "command=", command
		self.emit(QtCore.SIGNAL("compile_log"), "command", QtCore.QString(command))

		process.start(command)
		if process.waitForStarted(): 
			process.waitForFinished()
			result =  process.readAllStandardOutput()
			#print type(result), result
			error = process.readAllStandardError()
			#print type(error), error
			if error:
				self.emit(QtCore.SIGNAL("compile_log"), "error", QtCore.QString(error))
			else:
				self.emit(QtCore.SIGNAL("compile_log"), "result", QtCore.QString(result))


	def run_arduino_upload(self):
		self.emit(QtCore.SIGNAL("compile_log"), "start_upload", "%s" % self.file_to_compile)
		process = QtCore.QProcess(self)

		#arduino_path = settings.arduino_path()
		#if not arduino_path:
		#	self.set_error("Arduino root path not found", "..nothing to do ..")
			#TOD self.emit(
		#	return
		#print arduino_path.path()
		## ENV - Set Envoironment variables
		#env = QtCore.QStringList()
		#env << QtCore.QString("ARDUINO_DIR=").append(arduino_path.path())
		#env << QtCore.QString("ARDUINO_BOARD=").append(self.board)
		#env << QtCore.QString("ARDUINO_sPORT=").append(self.serial_port)
		#process.setEnvironment(env)
		#self.emit(QtCore.SIGNAL("compile_log"), "env", env.join(" "))
		#print "----------------------------------------"
		self.set_process_env(process)

		## Set "process path" to working dir Project Directory
		#project_dir = QtCore.QFileInfo(self.file_to_compile).absolutePath()
		#process.setWorkingDirectory(project_dir)
		#self.emit(QtCore.SIGNAL("compile_log"), "env", "cwd=" % project_dir)

		## construct the command "sh /app_path/etc/arduino_make.sh compile" and execute in project_dir dir
		command = QtCore.QString("sh ")
		#args = QtCore.QStringList()
		script_full_path = settings.app_path().absoluteFilePath("etc/arduino_make.sh compile upload")
		command.append(script_full_path)
		#print "command=", command
		self.emit(QtCore.SIGNAL("compile_log"), "command", QtCore.QString(command))

		process.start(command)
		if process.waitForStarted(): 
			process.waitForFinished()
			result =  process.readAllStandardOutput()
			#print type(result), result
			error = process.readAllStandardError()
			#print type(error), error
			if error:
				self.emit(QtCore.SIGNAL("compile_log"), "error", QtCore.QString(error))
			else:
				self.emit(QtCore.SIGNAL("compile_log"), "result", QtCore.QString(result))

