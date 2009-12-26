# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

#from gui.icons import Ico 
#from gui.icons import Icon 


class DEADHeaderWidget(QtGui.QDockWidget):

	def __init__(self, main):
		QtGui.QDockWidget.__init__(self)

		self.main = main

		containerWidget = QtGui.QWidget()
		self.setWidget(containerWidget)

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setContentsMargins(0,0,0,0)
		mainLayout.setSpacing(0)
		containerWidget.setLayout(mainLayout)

		label   = QtGui.QLabel("Arduino")
		label.setStyleSheet("background-color: black; color: white; font-size: 20pt;")

		mainLayout.addWidget(label)