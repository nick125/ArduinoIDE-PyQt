# -*- coding: utf-8 -*-

import yaml
from PyQt4 import QtCore

class FileOpenError(Exception): 
	"""
		Raised when there is an error opening a file
	"""
	pass

class Util:
	def get_file_contents(self, file_path):
		xFile = QtCore.QFile(file_path)
		if not xFile.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
			raise FileOpenError
		return QtCore.QString(xFile.readAll())

	def write_file(self, file_path, contents):
		file2Write = QtCore.QFile(file_path)
		if not file2Write.open(QtCore.QIODevice.WriteOnly | QtCore.QIODevice.Text):
			raise FileOpenError
		stream_out = QtCore.QTextStream(file2Write)
		stream_out << contents
		file2Write.close()


	def load_yaml(self, file_path):
		string = self.get_file_contents(file_path)
		return yaml.load(str(string))

		
	def load_arduino_config_file(self, file_path):
		#prog_file = self.main.settings.hardware_path().append("boards.txt")
		fileOb = QtCore.QFile(file_path)
		if not fileOb.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
			print "oops" # TODO error
			return False
		dic = {}
		## Parse foo.name = "xyx" and board.section.property = "xyx"

		## TODO - sort list
		while not fileOb.atEnd():
			line = fileOb.readLine()
			string =  QtCore.QString(line)
			string = string.trimmed()
			if string.length() > 0:
				if not string.startsWith("#"):
					if string.contains("."):
						pystr = str(string)
						kis_val = pystr.split("=")
						keys = kis_val[0].split(".")
						board_ki = keys[0]
						if not board_ki in dic:
							dic[board_ki] = {}

						 # 2 keys
						if len(keys) == 2:
							#self.boards_index.append({'board': kis_val[0], 'name': kis_val[1]})
							dic[board_ki][keys[1]]  = kis_val[1]

						# we got third value so section
						else: 
							if not keys[1] in dic[board_ki]:
								dic[board_ki][keys[1]] = {}
							dic[board_ki][keys[1]][keys[2]] = kis_val[1]

		return dic
