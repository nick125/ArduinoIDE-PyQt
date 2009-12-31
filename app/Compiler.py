# -*- coding: utf-8 -*-

class CompileCore(QtCore.QObject):



	def __init__(self, parent, board=None, port=None, compile_path=None, file_to_compile=None ):
		QtCore.QObject.__init__(self, parent)

		
	def compile(self, file_path):

		self.current_file_path = file_path
		self.progress.show()

		arduino_path = settings.arduino_path()
		if not arduino_path:
			self.set_error("Arduino root path not found", "..nothing to do ..")
			return
		## Set Envoironment
		env = QtCore.QStringList()
		env << QtCore.QString("ARDUINO_DIR=").append()
		env << QtCore.QString("ARDUINO_BOARD=").append("atmega328")
		env << QtCore.QString("ARDUINO_sPORT=").append("s/ssdev/ttyUSB0")
		self.process.setEnvironment(env)

		print "----------------------------------------"

		## Set working dir
		sketch_dir = QtCore.QFileInfo(self.current_file_path).absolutePath()
		
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
			self.process.waitForFinished()
			result =  self.process.readAllStandardOutput()
			#print type(result), result
			error = self.process.readAllStandardError()
			#print type(error), error
			if error:
				print "is error"
				self.actionIcon.setIcon(Icon(Ico.CompileError))
				self.statusLabel.setText("Error")
				self.textWidget.setPlainText(QtCore.QString(error))
			else:
				print "is ok"
				self.statusLabel.setText("OK")
				self.actionIcon.setIcon(Icon(Ico.CompileOk))
				self.textWidget.setPlainText(QtCore.QString(result))



		self.progress.hide()
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
