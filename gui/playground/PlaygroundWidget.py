# -*- coding: utf-8 -*-
"""
	A desperately miccelanious function and playground.. ;-))))))))))))))

	The idea here is that we demonstrate all the functionalitty of the Qt wioidget set..
	Buttons, timers etc..
	For some silly reason, its called a playground and can rip the code to make it work for u..
	

"""

from PyQt4 import QtCore, QtGui

from gui.icons import Ico 
from gui.icons import Icon 

from app.settings import settings

class PlayGroup(QtGui.QGroupBox):


	def __init__(self,  parent, title):
		QtGui.QGroupBox.__init__(self, parent)


class PlaygroundWidget(QtGui.QPushButton):
	def __init__(self,  parent, b_type):
		QtGui.QPushButton.__init__(self, parent)
		self.parent = parent
		self.setText(b_type)
		self.setIcon(Icon(Ico.Cancel))
		self.connect(self, QtCore.SIGNAL("clicked()"), parent.on_cancel)


		