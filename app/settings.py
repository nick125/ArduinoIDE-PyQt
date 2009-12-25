# -*- coding: utf-8 -*-
import os
import sys
from PyQt4 import QtCore, QtGui

import config


class Settings(QtCore.QObject):

	date_format = "dd-MM-yyyy"
	date_time_format = "dd-MM-yyyy HH:mm"


	def __init__(self):
		QtCore.QObject.__init__(self)

	
	def is_nix(self):
		return  'linux' in sys.platform


	def arduino_path(self):
		return QtCore.QString(config.ARDUINO_PATH)

	def app_path(self):
		## TODO - user QT settings
		return  QtCore.QString(os.path.abspath( os.path.dirname(__file__)	+  '/../' ))

	#def icon_path(self):
	#	return  os.path.abspath( os.path.dirname(__file__)	+  '/../../images/' )

	def help_path(self):
		return self.arduino_path().append("/reference/")

	def examples_path(self):
		return self.arduino_path().append("/examples/")

	def sketchbooks_path(self):
		return QtCore.QString(config.SKETCHBOOKS_PATH)

	def hardware_path(self):
		return self.arduino_path().append("/hardware/")
