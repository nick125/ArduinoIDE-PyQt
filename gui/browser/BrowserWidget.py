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
		act.setToolTip("Back")
		act = toolbar.addAction(Icon(Ico.Forward), "", self.on_forward)
		act.setToolTip("Forward")
		act = toolbar.addAction(Icon(Ico.Refresh), "", self.on_refresh)
		act.setToolTip("Refresh")

		self.txtUrl = QtGui.QLineEdit(initial_page)
		toolbar.addWidget(self.txtUrl)

		### Brwoser - declared below
		#self.browser = BrowserWidget(self, self.main, initial_page=initial_page, compact=compact, enable_api=enable_api)
		self.browser  = QtWebKit.QWebView(self)
		mainLayout.addWidget(self.browser, 2000)
		self.connect(self.browser, QtCore.SIGNAL("statusBarMessage(const QString&)"), self.on_browser_status_message)
		self.connect(self.browser, QtCore.SIGNAL("urlChanged(const QUrl&)"), self.on_browser_url_changed)
		self.connect(self.browser, QtCore.SIGNAL("linkClicked(QUrl&)"), self.on_browser_link_clicked)

		self.statusBar = QtGui.QStatusBar()
		mainLayout.addWidget(self.statusBar, 0)

		if initial_page:
			#print "INITIAL PAGE: %s" % initial_page
			self.browser.setUrl(QtCore.QUrl(QtCore.QString(initial_page)))

	def on_refresh(self):
		self.browser.reload()

	def on_back(self):
		self.browser.back()

	def on_forward(self):
		self.browser.forward()


	#################################################
	## Browser Events
	def on_browser_status_message(self, string):
		print "status=", string # does nothing ????
		self.statusBar.showMessage(string)

	def on_browser_url_changed(self, url): 
		return # doesnt trigger ???
		print "url=", url, url.toString()
		self.txtUrl.setText(url.toString())

	def on_browser_link_clicked(self, url):
		print "url=", url, url.toString() # doesnt trigger ???
		self.txtUrl.setText(url.toString())









class notUsed_atmo_BrowserWidget(QtWebKit.QWebView):
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


	
		
