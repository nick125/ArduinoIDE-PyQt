# -*- coding: utf-8 -*-

import yaml
from PyQt4 import QtCore

class Util:


	def iDEADcon(self, file_name):
		pass
	
	def get_file_contents(self, file_path):
		xFile = QtCore.QFile(file_path)
		if not xFile.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
			print "oops"
			return None
		return QtCore.QString(xFile.readAll())

	def write_file(self, file_path, contents):
		file2Write = QtCore.QFile(file_path)
		if not file2Write.open(QtCore.QIODevice.WriteOnly | QtCore.QIODevice.Text):
			print "TODO: error writing file"
			return
		stream_out = QtCore.QTextStream(file2Write)
		stream_out << contents
		file2Write.close()


	def load_yaml(self, file_path):
		string = self.get_file_contents(file_path)
		return yaml.load(str(string))

		