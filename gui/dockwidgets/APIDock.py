# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from gui.panes.APIBrowser import APIBrowser

class APIDockWidget(QtGui.QDockWidget):
	"""
		The main class for the API browser dock widget
	"""
	def __init__(self, parent, main):
		QtGui.QDockWidget.__init__(self)

		self.main = main

		containerWidget = QtGui.QWidget()
		self.setWidget(containerWidget)

		layout = QtGui.QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)
		containerWidget.setLayout(layout)	

		apiWidget = APIBrowser(self, self.main)
		layout.addWidget(apiWidget)



