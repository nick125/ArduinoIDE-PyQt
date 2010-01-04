# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from gui.icons import Ico 
from gui.icons import Icon 


# TODO - Addvalidators to the text

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

		toolbar = QtGui.QToolBar(self)
		toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		mainLayout.addWidget( toolbar )
	

		#self.actionAdd = toolbar.addAction(Icon(Ico.Help), "Add Site", self.on_add_site)
		#self.actionAddFunction.setDisabled(True)

		#self.actionEdit = toolbar.addAction(Icon(Ico.SiteEdit), "Edit Site", self.on_edit_site)
		#self.actionEdite.setDisabled(True)

		self.actionDelete = toolbar.addAction(Icon(Ico.Help), "Delete Site", self.on_delete_site)
		self.actionDelete.setDisabled(True)
		toolbar.addSeparator()

		self.tree = QtGui.QTreeWidget()
		mainLayout.addWidget(self.tree)
		self.tree.headerItem().setText(0, "Site")
		self.tree.headerItem().setText(1, "Url")

		
	def on_add_site(self):
		## TODO validate
		"""
		if self.txtTitle.text().trimmed().length() ==0:
			self.txtTitle.setFocus()
			return

		if self.txtUrl.text().trimmed().length() ==0:
			self.txtUrl.setFocus()
			return
		"""
		## validate URL _ check dupes
		dic = {	'title': str(self.txtTitle.text().trimmed()),
				'url':  str(self.txtUrl.text().trimmed())
				}
		
		yaml_string = yaml.dump(dic, Dumper=Dumper, default_flow_style=False)
		websites_file = settings.app_path().absoluteFilePath("etc/websites.yaml")
		print websites_file, yaml_string
		app.utils.write_file(websites_file, yaml_string)
		

	def load_project_settings(self):
		fileInfo = QtCore.QFileInfo(self.project_settings_file)
		if fileInfo.exists():
			self.project_settings =app.utils.load_yaml(self.project_settings_file)
		else:
			self.project_settings = None
	def on_delete_site(self):
		pass # TODO
