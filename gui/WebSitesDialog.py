# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from app.settings import settings
import app.utils

from gui.icons import Ico 
from gui.icons import Icon 


# TODO - Add validators to the url title

class WebSitesDialog(QtGui.QDialog):

	def __init__(self, parent, main):
		QtGui.QDialog.__init__(self, parent)
		self.main = main

		self.setWindowTitle("WebSites")
		self.setWindowIcon(Icon(Ico.Settings))
		self.setMinimumWidth(800)
		self.setMinimumHeight(500)

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)

		###############################
		## Add Website Group
		###############################
		grp = QtGui.QGroupBox("Add Website")
		mainLayout.addWidget(grp)
		grid = QtGui.QGridLayout()
		grp.setLayout(grid)
		
		row = 0
		grid.addWidget(QtGui.QLabel("Title"), row, 0, 1, 1, QtCore.Qt.AlignRight)
		self.txtTitle = QtGui.QLineEdit("title")
		self.txtTitle.setFixedWidth(400) ## WTF why this not expand
		grid.addWidget(self.txtTitle, row,  1, 1, 1, QtCore.Qt.AlignLeft)

		row += 1
		grid.addWidget(QtGui.QLabel("Url"), row, 0, 1, 1, QtCore.Qt.AlignRight)
		self.txtUrl = QtGui.QLineEdit("url")
		self.txtUrl.setFixedWidth(700) ## WTF why this not expand
		grid.addWidget(self.txtUrl, row, 1, 1, 2, QtCore.Qt.AlignLeft)

		row += 1
		butt = QtGui.QPushButton()
		butt.setText("Add")
		butt.setIcon(Icon(Ico.Save))
		self.connect(butt, QtCore.SIGNAL("clicked()"), self.on_add_site)
		grid.addWidget(butt, row, 2, 1, 2, QtCore.Qt.AlignRight)

		grid.setColumnStretch(0, 1)
		grid.setColumnStretch(1, 2)
		grid.setColumnStretch(2, 4)

		##############################################
		### Toolbar
		##############################################

		toolbar = QtGui.QToolBar(self)
		toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		mainLayout.addWidget( toolbar )
	
		self.actionDelete = toolbar.addAction(Icon(Ico.Help), "Delete Site", self.on_delete_site)
		self.actionDelete.setDisabled(True)
		toolbar.addSeparator()

		##############################################
		### Tree
		##############################################
		self.tree = QtGui.QTreeWidget()
		mainLayout.addWidget(self.tree)
		self.tree.headerItem().setText(0, "Site")
		self.tree.headerItem().setText(1, "Url")
		self.tree.setRootIsDecorated(False)

		############################
		### Storage
		self.websites_file = settings.app_path().absoluteFilePath("etc/websites.yaml")
		self.sites = None # list of sites
		self.load_sites()

	def load_sites(self):
		sites = app.utils.load_yaml(self.websites_file)
		print "load_sites", self.sites
		self.tree.model().removeRows(0, self.tree.model().rowCount())
		for site in sites:
			self.add_node(site['title'], site['url'])

	def add_node(self, title, url):
		item = QtGui.QTreeWidgetItem()
		item.setText(0, title)
		item.setText(1, url)
		self.tree.addTopLevelItem(item)	

	def on_add_site(self):
		## TODO validate
		if 1 == 0:
			if self.txtTitle.text().trimmed().length() ==0:
				self.txtTitle.setFocus()
				return

			if self.txtUrl.text().trimmed().length() ==0:
				self.txtUrl.setFocus()
				return
		self.add_node(str(self.txtTitle.text().trimmed()), str(self.txtUrl.text().trimmed()))
		
		self.save_sites()

	def save_sites(self):
		rootItem = self.tree.invisibleRootItem()
		sites = []
		for idx in range(0, rootItem.childCount()):
			item = rootItem.child(idx)
			sites.append({'title': str(item.text(0)), 'url': str(item.text(1))})
		app.utils.write_yaml(self.websites_file, sites)
		print sites, self.websites_file
		

	def on_delete_site(self):
		pass # TODO
