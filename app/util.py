# -*- coding: utf-8 -*-

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