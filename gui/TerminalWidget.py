# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui


from gui.icons import Ico 
from gui.icons import Icon 

class TerminalWidget(QtGui.QWidget):

	
	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self, parent)

		self.main = main

		self.currFile = None
		
		layout = QtGui.QVBoxLayout()
		layout.setContentsMargins(0,0,0,0)
		layout.setSpacing(0)
		self.setLayout(layout)

		self.headerLabel = QtGui.QLabel("Terminal Output")
		layout.addWidget(self.headerLabel)

		"""
		toolbar = QtGui.QToolBar()
		toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		layout.addWidget(toolbar)

		toolbar.addAction(Icon(Ico.Compile), "Compile")
		"""

		self.textWidget = QtGui.QPlainTextEdit()
		layout.addWidget(self.textWidget)
		self.textWidget.setDocumentTitle("Foo")
		self.textWidget.setStyleSheet("color: white; background-color: black;")