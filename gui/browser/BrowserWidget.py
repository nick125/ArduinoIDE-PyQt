# -*- coding: utf-8 -*-
"""
	Implements an internal QtWebKit based browser
"""

from PyQt4 import QtCore, QtGui, QtWebKit
from gui.browser.BrowserActions import BrowserActions

class Browser(QtWebKit.QWebView):
	"""
		Implements the internal browser
	"""
	def __init__(self, parent, main, initial_page=None, compact=False, enable_api=True):
		"""
			Initializes the internal browser
		"""
		QtWebKit.QWebView.__init__(self, parent)
		self.main = main
		if enable_api:
			self.actions = BrowserActions(main, self)

		if initial_page:
			self.setUrl(QtCore.QUrl(QtCore.QString(initial_page)))
	
		
