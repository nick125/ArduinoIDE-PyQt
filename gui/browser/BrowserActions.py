# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtWebKit

class BrowserActions(QtCore.QObject):
	"""
		Some functions to be exposed within WebKit
	"""
	def __init__(self, main, webview):
		"""
			Initializes BrowserActions
		"""
		QtCore.QObject.__init__(self)
		self.main = main
		self.webview = webview
		self.connect(self.webview.page().mainFrame(), QtCore.SIGNAL("javaScriptWindowObjectCleared()"), self, QtCore.SLOT("attach()"))

	#@QtCore.pyqtSlot() - temp removed as it caused an atribute aerror http://pastebin.ca/1737254
	def attach(self):
		self.webview.page().mainFrame().addToJavaScriptWindowObject(QtCore.QString("BrowserActions"), self)

	#@QtCore.pyqtSlot()   - temp removed as it caused an atribute aerror http://pastebin.ca/1737254
	def test_action(self):
		"""
			A test action
		"""
		print "Triggered!"
		return "Testing!"	
