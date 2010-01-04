# -*- coding: utf-8 -*-
"""
	Implements an internal QtWebKit based browser
"""

from PyQt4 import QtCore, QtGui, QtWebKit
from gui.browser.BrowserActions import BrowserActions


class Browser(QtGui.QWidget):

	def __init__(self, parent, main, initial_page=None, compact=False, enable_api=True):
		QtGui.QWidget.__init__(self, parent)

		self.main = main

		mainLayout = QtGui.QVBoxLayout()
		self.setLayout(mainLayout)

		self.browser = BrowserWidget(self, self.main, initial_page=initial_page, compact=compact, enable_api=enable_api)
		mainLayout.addWidget(self.browser)


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
			print "INITIAL PAGE: %s" % initial_page
			self.setUrl(QtCore.QUrl(QtCore.QString(initial_page)))
	
		
