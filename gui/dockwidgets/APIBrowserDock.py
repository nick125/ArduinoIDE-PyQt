# -*- coding: utf-8 -*-

"""
	Functions and classes related to the API Dock widget
"""

from PyQt4 import QtCore, QtGui

from gui.widgets.APIWidgets import APITreeWidget

class APIBrowserDock(QtGui.QDockWidget):
	"""
		The API dock widget
	"""
	
	def __init__(self, title, parent, main):
		"""
			Initializes the API dock widget
		"""
		QtGui.QDockWidget.__init__(self, title, parent)

		self.main = main

		containerWidget = QtGui.QWidget()
		self.setWidget(containerWidget)

		layout = QtGui.QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)
		containerWidget.setLayout(layout)	

		apiWidget = APITreeWidget(self, self.main)
		layout.addWidget(apiWidget)

