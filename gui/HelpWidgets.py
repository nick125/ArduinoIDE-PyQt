# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from gui.HelpBrowser import HelpBrowserDialog

from gui.icons import Ico 
from gui.icons import Icon 

import gui.widgets

class HelpDockWidget(QtGui.QDockWidget):

	
	def __init__(self, title, parent, main):
		QtGui.QDockWidget.__init__(self, title, parent)
		self.main = main

		self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)

		containerWidget = QtGui.QWidget()
		self.setWidget(containerWidget)

		layout = QtGui.QVBoxLayout()
		layout.setContentsMargins(0,0,0,0)
		layout.setSpacing(0)
		containerWidget.setLayout(layout)	

		helpWidget = HelpWidget(self, self.main)
		layout.addWidget(helpWidget)


class HelpWidget(QtGui.QWidget):

	
	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self)

		self.main = main

		layout = QtGui.QVBoxLayout()
		layout.setContentsMargins(0,0,0,0)
		layout.setSpacing(0)
		self.setLayout(layout)


		##################################################################
		##  Filter Bar
		##################################################################
		hBox = QtGui.QHBoxLayout()
		layout.addLayout(hBox)

		buttClearFilter = QtGui.QPushButton(self)
		buttClearFilter.setIcon( Icon(Ico.Black) )
		buttClearFilter.setFlat(True)
		buttClearFilter.setText("All")
		self.connect( buttClearFilter, QtCore.SIGNAL("clicked()"), self.on_filter_clear)
		hBox.addWidget( buttClearFilter, 1 )

		self.txtFilter = QtGui.QLineEdit("")
		self.connect(self.txtFilter, QtCore.SIGNAL('textChanged(const QString &)'), self.on_filter_changed)
		hBox.addWidget( self.txtFilter, 222 )

		
		##################################################################
		### Models
		##################################################################
		self.model = QtGui.QStandardItemModel(0, 1, self)
		self.model.setHeaderData(0, QtCore.Qt.Horizontal, QtCore.QVariant("Topic"))
		self.proxyModel = QtGui.QSortFilterProxyModel(self)
		self.proxyModel.setSourceModel( self.model )

		#################################################################
		### Tree
		##################################################################
		self.tree = QtGui.QTreeView()
		self.tree.setRootIsDecorated(False)
		self.tree.setAlternatingRowColors(True)
		self.tree.setSortingEnabled(True)
		self.tree.setModel(self.proxyModel)
		layout.addWidget(self.tree)
		self.connect(self.tree, QtCore.SIGNAL("clicked(const QModelIndex&)"), self.on_tree_double_clicked)


		self.statusWidget = gui.widgets.StatusWidget(self)
		self.load()

	####################################################
	## Filter related
	####################################################
	def on_filter_clear(self):
		self.txtFilter.setText("")
		self.txtFilter.setFocus()

	def on_filter_changed(self, filterString):
		self.proxyModel.setFilterKeyColumn(0)
		regExp = QtCore.QRegExp(self.txtFilter.text(), QtCore.Qt.CaseInsensitive)
		self.proxyModel.setFilterRegExp(regExp)

	####################################################
	## Load Files
	####################################################
	def load(self):
		pathStr = self.main.settings.help_path()
		print "LOAD HELP########ddd", pathStr
		if not pathStr:
			self.statusWidget.set_status(self.tree, "Path not found")
			return
		dirr = QtCore.QDir(pathStr)
		if not dirr.exists():
			QtGui.QMessageBox.information(self, "OOps", " the reference dir %s was not found" % pathStr)
			return
		## TODO - make this return *.html
		infoList = dirr.entryInfoList(QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot)
		for fileInfo in infoList:
			if fileInfo.suffix() == 'html':
				row_idx = self.model.rowCount()
				item = QtGui.QStandardItem( fileInfo.baseName() )
				item.setEditable(False)
				#item.setData( QtCore.QVariant(rec) )
				#item.setIcon( dIcon( dIco.Red ) if str(rec['online']) == '1' else dIcon( dIco.Black ) )
				self.model.setItem(row_idx, 0, item)
				#self.tree.sortByColumn(self.COLS.company, QtCore.Qt.AscendingOrder)
				#self.tree.header().setResizeMode( self.COLS.company, QtGui.QHeaderView.ResizeToContents )

				"""
				treeItem = QtGui.QTreeWidgetItem()
				treeItem.setText(0, fileInfo.baseName() ) ## hack to remove .html
				treeItem.setData(0, QtCore.Qt.UserRole, QtCore.QVariant( fileInfo.filePath() ))
				treeItem.setIcon(0, Icon(Ico.HelpDoc))
				self.tree.addTopLevelItem(treeItem)
				"""

	def on_tree_double_clicked(self, modelIndex):
		#print modelIndex
		item = self.model.itemFromIndex( self.proxyModel.mapToSource( modelIndex ) )
		#self.currDic =  self.main.ut.clean_dic(item.data().toPyObject())
		#self.account_id = int( self.currDic['account_id'] )
		#self.actionEdit.trigger()
		#print item.text(0), item.data(0, QtCore.Qt.UserRole).toString()
		page = item.data(QtCore.Qt.UserRole).toString()
		print page
		dialog = HelpBrowserDialog(self, self.main)
		dialog.load_help_page( page )
		dialog.show()