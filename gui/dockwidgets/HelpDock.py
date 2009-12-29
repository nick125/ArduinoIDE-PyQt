# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from gui.widgets.HelpWidgets import HelpTree

class HelpDock(QtGui.QDockWidget):
	"""
		The Help Dock Widget
	"""	
	def __init__(self, title, parent, main):
		"""
			Initializes the Help Dock Widget
		"""
		QtGui.QDockWidget.__init__(self, title, parent)

		self.main = main

		self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)

		containerWidget = QtGui.QWidget()
		self.setWidget(containerWidget)

		layout = QtGui.QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)
		containerWidget.setLayout(layout)	

		helpTree = HelpTree(self, self.main)
		layout.addWidget(helpTree)


