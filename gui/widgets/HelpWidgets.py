# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from gui.HelpBrowser import HelpBrowserDialog

from gui.icons import Ico 
from gui.icons import Icon 


from gui.widgets import GenericWidgets

# TODO somehow the test box need to focus first

class HelpTree(QtGui.QWidget):

	
	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self)

		self.main = main

		layout = QtGui.QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)
		self.setLayout(layout)


		##################################################################
		##  Filter Text bar
		##################################################################
		filterBarLayout = QtGui.QHBoxLayout()
		layout.addLayout(filterBarLayout)

		buttClearFilter = QtGui.QPushButton(self)
		buttClearFilter.setIcon( Icon(Ico.Black) )
		buttClearFilter.setFlat(True)
		buttClearFilter.setText("All")
		self.connect( buttClearFilter, QtCore.SIGNAL("clicked()"), self.on_filter_clear)
		filterBarLayout.addWidget( buttClearFilter, 1 )

		self.txtFilter = QtGui.QLineEdit("")
		self.connect(self.txtFilter, QtCore.SIGNAL('textChanged(const QString &)'), self.on_filter_changed)
		filterBarLayout.addWidget( self.txtFilter, 222 )

		##################################################################
		##  Filter Buttons
		##################################################################
		filterButtonsLayout = QtGui.QHBoxLayout()
		layout.addLayout(filterButtonsLayout)
		buttz = []
		buttz.append(['html', Ico.Html, "Html"])
		buttz.append(['functions', Ico.Functions, 'Functions'])
		buttz.append(['keywords',Ico.Help, 'Keywords'])
		filterButtonsGroup = QtGui.QButtonGroup(self)
		self.connect(filterButtonsGroup, QtCore.SIGNAL(""), self.on_filter_button_clicked)
		for ki, ico, caption in buttz:
			newButton = QtGui.QPushButton()
			newButton.setText(caption)
			newButton.setIcon(Icon(ico))
			newButton.setCheckable(True)
			newButton.setChecked(True if ki == 'functions' else False) # TODO remember last view
			## TODO restore state
			filterButtonsLayout.addWidget(newButton)


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
		self.connect(self.tree, QtCore.SIGNAL("doubleClicked(const QModelIndex&)"), self.on_tree_double_clicked)


		self.statusWidget = GenericWidgets.StatusWidget(self)
		self.load_list()

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
	def load_list(self):
		xlist = self.main.api.list()
		for entry_type, file_path, entry, ico in xlist:
			print entry_type, entry
			if entry_type == 'function':
				row_idx = self.model.rowCount()
				item = QtGui.QStandardItem( entry )
				item.setIcon(Icon(ico))
				item.setEditable(False)
				self.model.setItem(row_idx, 0, item)
				itemki = item = QtGui.QStandardItem( entry_type )
				self.model.setItem(row_idx, 1, itemki)
		self.tree.sortByColumn(0, QtCore.Qt.AscendingOrder)	

	def on_tree_double_clicked(self, modelIndex):
		## TOD open HTML or API
		item = self.model.itemFromIndex( self.proxyModel.mapToSource( modelIndex ) )
		page = item.data(QtCore.Qt.UserRole).toString()
		dialog = HelpBrowserDialog(self, self.main)
		dialog.load_help_page( page )
		dialog.show()

	def on_filter_button_clicked(self, butt):
		print butt