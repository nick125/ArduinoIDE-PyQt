# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui, QtWebKit
from gui.browser.BrowserActions import BrowserActions

### Pete notes ? ? does this needs to be a functional brower panel


class Browser(QtWebKit.QWebView):
	def __init__(self, parent, main, initial_page=None, compact=False, enable_api=True):
		QtWebKit.QWebView.__init__(self, parent)
		self.main = main
		if enable_api:
			self.actions = BrowserActions(main, self)

		if initial_page:
			self.setUrl(QtCore.QUrl(QtCore.QString(initial_page)))
	
		
