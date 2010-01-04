# -*- coding: utf-8 -*-
"""
	Implements an internal QtWebKit based browser
"""

from PyQt4 import QtCore, QtGui, QtWebKit
from gui.browser.BrowserActions import BrowserActions

from gui.icons import Ico 
from gui.icons import Icon 


class Browser(QtGui.QWidget):

	def __init__(self, parent, main, initial_page=None, compact=False, enable_api=True):
		QtGui.QWidget.__init__(self, parent)

		self.main = main

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setContentsMargins(0,0,0,0)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)

		toolbar = QtGui.QToolBar()
		mainLayout.addWidget(toolbar, 0)

		act = toolbar.addAction(Icon(Ico.Back), "", self.on_back)
		act = toolbar.addAction(Icon(Ico.Forward), "", self.on_forward)
		act = toolbar.addAction(Icon(Ico.Refresh), "", self.on_refresh)

		self.txtUrl = QtGui.QLineEdit(initial_page)
		toolbar.addWidget(self.txtUrl)

		### Brwoser - declared below
		self.browser = BrowserWidget(self, self.main, initial_page=initial_page, compact=compact, enable_api=enable_api)
		mainLayout.addWidget(self.browser, 2000)

		self.statusBar = QtGui.QStatusBar()
		mainLayout.addWidget(self.statusBar, 0)

	def on_refresh(self):
		self.statusBar.showMessage("TODO", 2000)

	def on_back(self):
		self.statusBar.showMessage("TODO", 2000)

	def on_forward(self):
		self.statusBar.showMessage("TODO", 2000)


class BrowserWidget(QtWebKit.QWebView):
	"""
		Implements the internal browser
	"""
	def __init__(self, parent, main, initial_page=None, compact=False, enable_api=True):
		"""
			Initializes the internal browser
		"""
		QtWebKit.QWebView.__init__(self, parent)
		self.main = main
		#if enable_api:  - temp removed - http://pastebin.ca/1737254
		#	self.actions = BrowserActions(main, self)

		if initial_page:
			#print "INITIAL PAGE: %s" % initial_page
			self.setUrl(QtCore.QUrl(QtCore.QString(initial_page)))
	
		
