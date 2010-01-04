# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from app.settings import settings
import app.utils

from gui.icons import Ico 
from gui.icons import Icon 


# TODO - Add validators to the url title

class WebSitesDialog(QtGui.QDialog):

	class COLS:
		group = 0
		title = 1
		url = 2

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
		grid.addWidget(QtGui.QLabel("Group"), row, 0, 1, 1, QtCore.Qt.AlignRight)
		self.comboGroup = QtGui.QComboBox()
		self.comboGroup.addItem("Arduino")
		self.comboGroup.addItem("arduino-pyqt")
		self.comboGroup.addItem("Other")
		self.comboGroup.setFixedWidth(400) ## WTF why this not expand
		grid.addWidget(self.comboGroup, row,  1, 1, 1, QtCore.Qt.AlignLeft)

		buttAddGroup = QtGui.QToolButton()
		buttAddGroup.setIcon(Icon(Ico.Add))
		buttAddGroup.setText("New Group")
		self.connect(buttAddGroup, QtCore.SIGNAL("clicked()"), self.on_add_group)
		grid.addWidget(buttAddGroup, row,  2, 1, 1, QtCore.Qt.AlignLeft)
	
		row += 1
		grid.addWidget(QtGui.QLabel("Title"), row, 0, 1, 1, QtCore.Qt.AlignRight)
		self.txtTitle = QtGui.QLineEdit("")
		self.txtTitle.setFixedWidth(400) ## WTF why this not expand
		grid.addWidget(self.txtTitle, row,  1, 1, 1, QtCore.Qt.AlignLeft)

		row += 1
		grid.addWidget(QtGui.QLabel("Url"), row, 0, 1, 1, QtCore.Qt.AlignRight)
		self.txtUrl = QtGui.QLineEdit("")
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
		self.tree.headerItem().setText(self.COLS.group, "Group")
		self.tree.headerItem().setText(self.COLS.title, "Title")
		self.tree.headerItem().setText(self.COLS.url, "Address")
		self.tree.setRootIsDecorated(True)
		self.connect( self.tree, QtCore.SIGNAL("itemSelectionChanged()"), self.on_tree_selection_changed)
		self.connect( self.tree, QtCore.SIGNAL("itemClicked(QTreeWidgetItem *,int)"), self.on_tree_item_clicked)
		self.connect( self.tree, QtCore.SIGNAL("itemChanged (QTreeWidgetItem *,int)"), self.save_sites)
		

		############################
		### Storage
		self.websites_file = settings.app_path().absoluteFilePath("etc/websites.yaml")
		self.sites = None # list of sites
		self.load_sites()

	def load_sites(self):	
		self.tree.model().removeRows(0, self.tree.model().rowCount())
		groups = app.utils.load_yaml(self.websites_file)
		if not groups:
			return
		for grp in groups:
			idx = self.comboGroup.findText(grp, QtCore.Qt.MatchExactly)
			if idx == -1:
				self.comboGroup.addItem(grp)
			for site in groups[grp]:
				self.add_node(grp, site['title'], site['url'])

	def add_node(self, group, title, url):
		items = self.tree.findItems(group, QtCore.Qt.MatchExactly, self.COLS.group)
		if len(items) > 0:
			grpItem = items[0]
		else:
			grpItem = QtGui.QTreeWidgetItem()
			grpItem.setText(self.COLS.group, group)
			grpItem.setFirstColumnSpanned(True)
			grpItem.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled )
			self.tree.addTopLevelItem(grpItem)
			self.tree.setItemExpanded(grpItem, True)		
		item = QtGui.QTreeWidgetItem(grpItem)
		item.setText(self.COLS.title, title)
		item.setText(self.COLS.url, url)
		item.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
		

	def on_add_site(self):
		## TODO validate
		if self.txtTitle.text().trimmed().length() ==0:
			self.txtTitle.setFocus()
			return

		if self.txtUrl.text().trimmed().length() ==0:
			self.txtUrl.setFocus()
			return
		self.add_node(	str(self.comboGroup.currentText()),
						str(self.txtTitle.text().trimmed()), 
						str(self.txtUrl.text().trimmed())
					)
		self.txtTitle.setText("")
		self.txtUrl.setText("")
		self.save_sites()

	####################################
	### Save Sites
	def save_sites(self):
		rootItem = self.tree.invisibleRootItem()
		groups = {}
		for gidx in range(0, rootItem.childCount()):
			groupItem = rootItem.child(gidx)
			grp = str(groupItem.text(self.COLS.group))
			if not grp in groups:
				groups[grp] = []
			for idx in  range(0, groupItem.childCount()):
				item = groupItem.child(idx)
				dic = {'title': str(item.text(self.COLS.title)), 'url': str(item.text(self.COLS.url))}
				groups[grp].append(dic)
		app.utils.write_yaml(self.websites_file, groups)
		self.emit(QtCore.SIGNAL("websites_changed"))

		
	####################################
	### Delete Site
	def on_delete_site(self):
		item = self.tree.currentItem()
		self.tree.invisibleRootItem().removeChild(item)	
		self.save_sites()

	####################################
	### Tree Events
	def on_tree_item_clicked(self, item):
		pass

	def on_tree_selection_changed(self):
		self.actionDelete.setEnabled(self.tree.selectionModel().hasSelection())

	def on_add_group(self):
		new_group, ok = QtGui.QInputDialog.getText(self, "New Group", "Enter group name")
		if ok:
			new_group = new_group.trimmed()
			if new_group.length() > 0:
				idx = self.comboGroup.count()
				self.comboGroup.addItem(new_group)
				self.comboGroup.setCurrentIndex(idx)
				