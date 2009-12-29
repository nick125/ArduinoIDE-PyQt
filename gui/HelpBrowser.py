# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui, QtWebKit

import gui.HelpWidgets
import gui.widgets
from gui.icons import Icon
from gui.icons import Ico
	
##########################################################################
## Help Dialog
##########################################################################	
	
class HelpBrowserDialog(QtGui.QDialog):

	def __init__(self, parent, main):
		QtGui.QDialog.__init__(self, parent)
		self.main = main

		self.setWindowIcon(Icon(Ico.Help))
		self.setWindowTitle("Help")
		self.setMinimumWidth(800)
		self.setMinimumHeight(500)

		self.statusLabel = gui.widgets.StatusLabel(self)

		layout = QtGui.QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)
		self.setLayout( layout )

		splitter = QtGui.QSplitter(self)
		layout.addWidget(splitter)

		self.helpTree = gui.HelpWidgets.HelpTree(self, self.main)
		splitter.addWidget(self.helpTree)
		#splitter.setStretchFactor(0, 1)

		self.browser = QtWebKit.QWebView()
		splitter.addWidget( self.browser )
		#splitter.setStretchFactor(0, 5)

	def load_help_page(self, page):
		url_str = QtCore.QString("file://").append(page)
		self.browser.load(QtCore.QUrl(url_str))
