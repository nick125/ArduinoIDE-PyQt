# -*- coding: utf-8 -*-

from operator import itemgetter

from PyQt4 import QtCore

class Boards(QtCore.QObject):

	def __init__(self, parent):
		QtCore.QObject.__init__(self, parent)

		self.main = parent

		self.current_board = None
		self.boards_index = None
		self.boards_tree = None

		self.load()

	def load(self):
		self.boards_index = {}
		self.boards_tree = {}
		prog_file = self.main.settings.hardware_path().append("boards.txt")
		if not prog_file:
			return

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
							self.boards_index[keys[0]] = kis_val[1]
							self.boards_tree[board_ki][keys[1]]  = kis_val[1]

						# we got third value so section
						else: 
							if not keys[1] in self.boards_tree[board_ki]:
								self.boards_tree[board_ki][keys[1]] = {}
							self.boards_tree[board_ki][keys[1]][keys[2]] = kis_val[1]

	def index(self):
		items = self.boards_index.items()
		items.sort(key=itemgetter(1))
		return items

	def set_current(self, board):
		self.main.settings.setValue("current_board", board)
		self.current_board = {'board': board, 'name': self.boards_index[str(board)]}
		self.emit(QtCore.SIGNAL("board_selected"), self.current_board)
		return self.current_board

	def current(self):
		return self.current_board

	def all(self):
		return self.boards_tree # [str(board)] 

