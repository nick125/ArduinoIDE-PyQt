# -*- coding: utf-8 -*-
import os
import sys
from PyQt4 import QtCore, QtGui

import config

"""
Quick Notes

Class that is rooted to this __file__
parent = app_root is expected to be parent on this.
This objject is shared globally as self.main.settings.*

For some mad reason I want to push the "path" requests though this class.. so its all in one place..

"""

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

	def icons_path(self):
		return  self.app_path().append("/images/icons/")

	def help_path(self):
		return self.arduino_path().append("/reference/")

	def examples_path(self):
		return self.arduino_path().append("/examples/")

	def sketchbooks_path(self):
		return QtCore.QString(config.SKETCHBOOKS_PATH)

	def hardware_path(self):
		return self.arduino_path().append("/hardware/")

	def keywords_path(self):
		return self.app_path().append("/keywords")

	def def_path(self):
		return self.app_path().append("/etc/def")