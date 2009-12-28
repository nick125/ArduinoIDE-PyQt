# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from gui.icons import Ico 
from gui.icons import Icon 

###########################################################################################
## Buttons
###########################################################################################

## Cancel
class CancelButton(QtGui.QPushButton):
	def __init__(self,  parent, b_type):
		QtGui.QPushButton.__init__(self, parent)
		self.parent = parent
		self.setText(b_type)
		self.setIcon(Icon(Ico.Cancel))
		self.connect(self, QtCore.SIGNAL("clicked()"), parent.on_cancel)

## Help
class HelpButton(QtGui.QPushButton):
	def __init__(self,  parent, page):
		QtGui.QPushButton.__init__(self, parent)
		self._page = page	
		self.setToolTip("Show help")
		self.setFlat(True)
		self.setIcon(Icon(Ico.Help))
		self.connect(self, QtCore.SIGNAL("clicked()"), self.on_help)

	def set_help(self, page):
		self._page = page

	def on_help(self):
		d = HelpDialog(self)
		d.show_help(self._page)

## Refresh
class RefreshButton(QtGui.QPushButton):
	def __init__(self,  parent, label=None):
		QtGui.QPushButton.__init__(self, parent)
		self.parent = parent
		self.setIcon( Icon(Ico.Refresh2) )
		self.setFlat(True)
		self.setStyleSheet("padding: 0px;")
		self.connect(self, QtCore.SIGNAL("clicked()"), parent.on_refresh)

## Save
class SaveButton(QtGui.QPushButton):
	def __init__(self,  parent, label=None, sending=None, done=None):
		QtGui.QPushButton.__init__(self, parent)
		self.parent = parent
		self.setMinimumWidth(100)
		self.setText(label if label else "Save")
		self.setIcon(Icon(Ico.Save))
		self.connect(self, QtCore.SIGNAL("clicked()"), parent.on_save)

	def set_dirty(self, state=True):
		self.setStyleSheet("color: %s;" % '#990000' if state else 'black')



class ToolBarSpacer( QtGui.QWidget ):

	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		sp = QtGui.QSizePolicy()
		sp.setHorizontalPolicy( QtGui.QSizePolicy.Expanding )
		self.setSizePolicy( sp )


class StatusLabel(QtGui.QWidget):

	def __init__(self, parent, label=None):
		QtGui.QWidget.__init__(self, parent)

		
		mainLayout = QtGui.QHBoxLayout()
		mainLayout.setContentsMargins(0,0,0,0)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)

		if label:
			self.lblC = QtGui.QLabel(label + ":")
			self.lblC.setAlignment(QtCore.Qt.AlignRight)
			self.lblC.setStyleSheet("border: 1px outset transparent;")
			mainLayout.addWidget(self.lblC)

		self.labelVal = QtGui.QLabel("Foo")
		self.labelVal.setStyleSheet("border: 1px outset #eeeeee;")
		mainLayout.addWidget(self.labelVal)

	def setText(self, txt):
		self.labelVal.setText(txt)

#####################################################################################################################
## Header Label
#####################################################################################################################
class HeaderLabel( QtGui.QWidget ):

	def __init__(self, parent, main, icon=None, title="Foo", wash_to="black", color="black", background="white"):
	#def __init__(self, configVars, parent):
		QtGui.QWidget.__init__(self, parent)

		#self.config = configVars
		self.main = main
		self.background = background
		#self.img_dir = main.settin
		
		#########################################################
		## Container Layout
		mainLayout = QtGui.QHBoxLayout()
		#mainLayout = QtGui.QGridLayout()
		mainLayout.setSpacing(0)
		mainLayout.setContentsMargins(0,0,0,0)
		self.setLayout( mainLayout )

		#self.width_height = 22 if self.lines == 2 else 16

		#########################################################
		## mainWidget Container widget
		mainWidget = QtGui.QWidget()
		mainLayout.addWidget( mainWidget )
		mainWidget.setStyleSheet( "background-color: %s; padding: 0px; margin: 0px;" % (self.background) )


		### Main Box accross
		mainHBox  = QtGui.QHBoxLayout()
		mainHBox.setSpacing(0)
		m = 0
		mainHBox.setContentsMargins(m,m,m,m)
		mainHBox.setSpacing(0)
		mainWidget.setLayout( mainHBox )


		### Icon Widget
		self.iconWidget = QtGui.QLabel()
		self.iconWidget.setStyleSheet("background: transparent; padding: 0px; margin: 0px; ")
		self.iconWidget.setPixmap( self.get_pixmap(icon , 16) )
		self.iconWidget.setContentsMargins( 10, 0, 0, 0 )
		mainHBox.addWidget(  self.iconWidget, 0 )

		### Vertical Box for Labels
		vLabelBox = QtGui.QVBoxLayout()
		vLabelBox.setContentsMargins(10, 5, 0, 5 )
		mainHBox.addLayout( vLabelBox, 1 )

		
		### Main Label
		self.mainLabel = QtGui.QLabel(title)
		self.mainLabel.setStyleSheet("padding: 0px; margin: 0px;  font-weight: bold; color: %s; font-size: 10pt" % (color)  )
		vLabelBox.addWidget( self.mainLabel )

		### Sub Label
		#if self.lines == 2:
			#self.subLabel = QtGui.QLabel(self.sub_title)
			#self.subLabel.setStyleSheet(" font-size: 7em; color: %s;" % self.sub_color)
			#vLabelBox.addWidget( self.subLabel)

		### Gradient albel
		
		self.gradientLabel = QtGui.QLabel()
		self.gradientLabel.setMinimumWidth(50)
		self.gradientLabel.setMaximumWidth(100)
		mainHBox.addWidget(  self.gradientLabel, 1 )
		self.set_gradient(wash_to)

	def set_gradient(self, wash_color):
		style_grad = "background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 %s, stop: 1 %s);" % (self.background, wash_color)
		self.gradientLabel.setStyleSheet(style_grad)

	def get_pixmap(self, ico, wh):
		pixmap = QtGui.QPixmap( self.main.settings.icons_path().append(ico) )
		return pixmap.scaled(wh, wh, QtCore.Qt.IgnoreAspectRatio)

	def setHeaders( self, txt, txt_small = None ):
		self.mainLabel.setText(txt)
		if txt_small and self.lines == 2:
			self.subLabel.setText(txt_small)

	def setTitle(self, txt):
		self.mainLabel.setText( txt )


	def setSubTitle(self, txt):
		self.subLabel.setText( txt )

	def setIcon(self, icon, wid_hei=None):
		self.iconWidget.setPixmap( self.get_pixmap(icon, wid_hei if wid_hei else self.width_height) )



