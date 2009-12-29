# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from gui.HelpBrowser import HelpBrowser

from gui.icons import Ico 
from gui.icons import Icon 

class DDDHelpWidget(QtGui.QDockWidget):

	
	def __init__(self, main=None):
		QtGui.QDockWidget.__init__(self)

		self.main = main

		containerWidget = QtGui.QWidget()
		self.setWidget(containerWidget)

		layout = QtGui.QVBoxLayout()
		layout.setContentsMargins(0,0,0,0)
		layout.setSpacing(0)
		containerWidget.setLayout(layout)

		lblTitle = QtGui.QLabel("Help")
		lblTitle.setStyleSheet("font-weight: bold; border: 2px outset yellow; background-color: green; color: white; padding: 5px;")
		layout.addWidget(lblTitle)

		self.tree = QtGui.QTreeWidget()
		self.tree.setRootIsDecorated(False)
		self.tree.setAlternatingRowColors(True)
		layout.addWidget(self.tree)
		self.connect(self.tree, QtCore.SIGNAL("itemDoubleClicked (QTreeWidgetItem *,int)"), self.on_tree_double_clicked)

		self.tree.headerItem().setText(0, "Topic")

		self.load_files()

	def load_files(self):
		pathStr = self.main.settings.help_path()
		dirr = QtCore.QDir(pathStr)
		if not dirr.exists():
			QtGui.QMessageBox.information(self, "OOps", " the reference dir %s was not found" % pathStr)
			return
		## TODO - make this return *.html
		infoList = dirr.entryInfoList(QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot)
		for fileInfo in infoList:
			if fileInfo.suffix() == 'html':
				treeItem = QtGui.QTreeWidgetItem()
				treeItem.setText(0, fileInfo.baseName() ) ## hack to remove .html
				treeItem.setIcon(0, Icon(Ico.HelpDoc))
				self.tree.addTopLevelItem(treeItem)

	def on_tree_double_clicked(self, item, column):
		print item, column
	