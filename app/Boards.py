# -*- coding: utf-8 -*-

from PyQt4 import QtCore

class Boards:

	def __init__(self, main):
		self.main = main

		self.boards_index = []
		self.boards_tree = {}

		prog_file = self.main.settings.hardware_path().append("boards.txt")
		progFile = QtCore.QFile(prog_file)
		if not progFile.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
			print "oops" # TODO error
			return
		dic = {}
		## Parse board.name = "xyx" and board.section.property = "xyx"

		## TODO - sort list
		while not progFile.atEnd():
			line = progFile.readLine();
			string =  QtCore.QString(line)
			string = string.trimmed()
			if string.length() > 0:
				if not string.startsWith("#"):
					if string.contains("."):
						pystr = str(string)
						kis_val = pystr.split("=")
						keys = kis_val[0].split(".")
						board_ki = keys[0]
						if not board_ki in self.boards_tree:
							self.boards_tree[board_ki] = {}

						 # 2 keys
						if len(keys) == 2:
							self.boards_index.append({'board': kis_val[0], 'name': kis_val[1]})
							self.boards_tree[board_ki][keys[1]]  = kis_val[1]

						# we got third value so section
						else: 
							if not keys[1] in self.boards_tree[board_ki]:
								self.boards_tree[board_ki][keys[1]] = {}
							self.boards_tree[board_ki][keys[1]][keys[2]] = kis_val[1]

		#print "------------------------------------"
		#print self.boards_index

	def index(self):
		return self.boards_index

	def data(self):
		return self.boards_tree

	def test(self):
		
		for b in self.boards:
			print "Boards=--------------------------"
			print b
			for x in self.boards[b]:
				print x, self.boards[b][x]

class Programmers:

	def __init__(self, main):
		self.main = main

		self.programmers = QtCore.QStringList()

		prog_file = self.main.settings.hardware_path().append("programmers.txt")
		progFile = QtCore.QFile(prog_file)
		if not progFile.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
			print "oops"
			return
		
		while not progFile.atEnd():
			line = progFile.readLine();
			string =  QtCore.QString(line)
			string = string.trimmed()
			if string.length() > 0:
				if string.contains(".name="):
					parts = string.split("=")
					board_name = parts[1].trimmed()
					self.programmers.append( board_name )

	def index(self):
		return self.programmers
		
