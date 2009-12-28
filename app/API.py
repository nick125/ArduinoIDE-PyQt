# -*- coding: utf-8 -*-

from operator import itemgetter
from PyQt4 import QtCore

class API(QtCore.QObject):

	def __init__(self, main):
		QtCore.QObject.__init__(self, main)

		self.main = main

	def html_index(self)
		pathStr = self.main.settings.help_path()
		dirr = QtCore.QDir(pathStr)
		if not dirr.exists():
			#QtGui.QMessageBox.information(self, "OOps", " the reference dir %s was not found" % pathStr)
			print "error"
			return

		

