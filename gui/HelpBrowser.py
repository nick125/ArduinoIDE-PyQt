# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui, QtWebKit

from gui.icons import Icon
from gui.icons import Ico
	
##########################################################################
## Help Dialog
##########################################################################	
	
class HelpBrowser(QtGui.QWidget):

	def __init__(self, parent):
		QtGui.QWidget.__init__(self, parent)

		self.setWindowIcon(dIcon(dIco.Help))
		self.setWindowTitle("Help")
		self.setMinimumWidth(500)
		self.setMinimumHeight(500)

		layout = QtGui.QVBoxLayout()
		self.setLayout( layout )

		self.browser = QtWebKit.QWebView()
		layout.addWidget( self.browser )

		