# -*- coding: utf-8 -*-
"""
	Implements an internal QtWebKit based browser
"""

from PyQt4 import QtCore, QtGui, QtWebKit
from gui.browser.BrowserActions import BrowserActions

from gui.icons import Ico 
from gui.icons import Icon 


class BrowserPane(QtGui.QWidget):
	"""
		Implements a Browser pane
	"""

	def __init__(self, parent, main, initial_page=None, compact=False, enable_api=True, auto_compact_exit=True):
		"""
			Initializes the browser pane 
		"""
		QtGui.QWidget.__init__(self, parent)

		self.main = main
		self.compact = compact
		self.auto_compact_exit = auto_compact_exit

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setContentsMargins(0,0,0,0)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)

		self.toolbar = QtGui.QToolBar()
		mainLayout.addWidget(self.toolbar, 0)

		act = self.toolbar.addAction(Icon(Ico.Back), "", self.on_back)
		act.setToolTip("Back")
		act = self.toolbar.addAction(Icon(Ico.Forward), "", self.on_forward)
		act.setToolTip("Forward")
		act = self.toolbar.addAction(Icon(Ico.Refresh), "", self.on_refresh)
		act.setToolTip("Refresh")

		self.txtUrl = QtGui.QLineEdit(initial_page)
		self.toolbar.addWidget(self.txtUrl)
	
		### Brwoser - declared below
		self.browser = BrowserWidget(self, self.main, enable_api=enable_api)
		mainLayout.addWidget(self.browser, 2000)

		self.browser.statusBarMessage.connect(self.on_browser_status_message)
		self.browser.urlChanged.connect(self.on_browser_url_changed)
		self.browser.linkClicked.connect(self.on_browser_link_clicked)
		print "Connected Events"
		self.statusBar = QtGui.QStatusBar()
		mainLayout.addWidget(self.statusBar, 0)

		if compact:
			self.mode_change(compact)

		if initial_page:
			self.browser.setUrl(QtCore.QUrl(QtCore.QString(initial_page)))

	def mode_change(self, mode):
		"""
			Changes the mode of the browser from/into compact mode.
			
			Compact mode removes the toolbar and the status bar.
		"""
		if mode:
			self.toolbar.hide()
			self.statusBar.hide()
		else:
			self.toolbar.show()
			self.statusBar.show()

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
		print "URl Changed"
		if self.auto_compact_exit:
			self.change_mode(False)
		self.txtUrl.setText(url.toString())

	def on_browser_link_clicked(self, url):
		print "url=", url, url.toString() # doesnt trigger ???
		self.txtUrl.setText(url.toString())

class BrowserWidget(QtWebKit.QWebView):
	"""
		Implements the internal browser
	"""
	def __init__(self, parent, main, enable_api=True):
		"""
			Initializes the internal browser
		"""
		QtWebKit.QWebView.__init__(self, parent)
		self.main = main

		if enable_api:
			self.actions = BrowserActions(main, self)

