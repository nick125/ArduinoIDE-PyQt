# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from gui.icons import Ico 
from gui.icons import Icon 

class WebSitesDialog(QtGui.QDialog):

	def __init__(self, parent, main):
		QtGui.QDialog.__init__(self, parent)
		self.main = main

		self.setWindowTitle("WebSites")
		self.setWindowIcon(Icon(Ico.Settings))
		self.setMinimumWidth(700)
		self.setMinimumHeight(500)

		mainLayout = QtGui.QVBoxLayout()
		self.setLayout(mainLayout)

		toolbar = QtGui.QToolBar(self)
		toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		mainLayout.addWidget( toolbar )
	
		self.actionAdd = toolbar.addAction(Icon(Ico.SiteAdd), "Add Site", self.on_add_site)
		#self.actionAddFunction.setDisabled(True)

		#self.actionEdit = toolbar.addAction(Icon(Ico.SiteEdit), "Edit Site", self.on_edit_site)
		#self.actionEdite.setDisabled(True)

		self.actionDelete = toolbar.addAction(Icon(Ico.SiteDelete), "Delete Site", self.on_delete_site)
		self.actionDelete.setDisabled(True)
		toolbar.addSeparator()

		self.tree = QtGui.QTreeWidget()
		mainLayout.addWidget(self.tree)

		