# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

class Programmers:


	def __init__(self, main):
		self.main = main

		self.boards = QtCore.QStringList()

		prog_file = self.main.settings.hardware_path().append("programmers.txt")
		#arduino_path().append("/hardware/programmers.txt")
		print prog_file
		progFile = QtCore.QFile(prog_file)
		if not progFile.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
			print "oops"
			return
		
		while not progFile.atEnd():
			line = progFile.readLine();
			#process_line(line);
			string =  QtCore.QString(line)
			string = string.trimmed()
			if string.length() > 0:
				#print ">", string
				if string.contains(".name="):
					parts = string.split("=")
					board_name = parts[1].trimmed()
					self.boards.append( board_name )

	def index(self):
		return self.boards
			

			#else:
				#print "..."
		
