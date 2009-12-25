# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtWebKit

class Browser(QtWebKit.QWebView):

	def __init__(self, parent, main, page=None):
		QtWebKit.QWebView.__init__(self, parent)
		self.main = main

		if page:
			html_file_name = self.main.settings.app_path().append("/etc/welcome.html")
			print html_file_name


			html_str = self.main.ut.get_file_contents(html_file_name)
			to_do_file_name = self.main.settings.app_path().append("/README")
			readme = self.main.ut.get_file_contents(to_do_file_name)
			print readme
			print html_str.replace("###__README__###", readme)
			self.setHtml(html_str)
			self.show()

			