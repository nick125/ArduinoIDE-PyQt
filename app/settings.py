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

		self.qSettings = QtCore.QSettings("arduino-pyqt", "arduino-pyqt")
	

	def is_nix(self):
		return  'linux' in sys.platform

	#################################################
	## Proxy for QSettings class
	#################################################
	def value(self, ki, as_string=True):
		v = self.qSettings.value( ki )
		if v.isNull():
			return None
		if as_string:
			return v.toString()
		return v

	def setValue(self, ki, valu ):
		return self.qSettings.setValue( ki, QtCore.QVariant(valu) )

	def remove(self, ki):
		self.qSettings.remove(ki)



	#########################################################
	## Paths
	#########################################################
	def check_path(self, file_path):
		d = QtCore.QFileInfo(file_path)
		if d.exists():
			return file_path
		return None

	## Arduino Root
	def arduino_path(self):
		## TODO - use prefs
		#print "-----------------------"
		#print "path/arduino_roots", self.value("path/arduino_root").toString()
		return self.value("path/arduino_root")
		#print "str", v.toString(), "none:", v.isNull()
		#return v.toString()

	def arduino_svn_path(self):
		## TODO - use prefs
		print "path/arduino_svn", self.value("path/arduino_svn")
		return None

	def app_path(self):
		## TODO - user QT Object
		return  QtCore.QString(os.path.abspath( os.path.dirname(__file__)	+  '/../' ))

	def icons_path(self):
		return  self.app_path().append("/images/icons/")

	def hardware_path(self, append_str=None):
		if not self.arduino_path():
			return None
		path = self.arduino_path().append("/hardware/")
		if append_str:
			return self.check_path(path.append(append_str))
		return self.check_path(path)


	def help_path(self):
		if not self.arduino_path():
			return None
		return self.arduino_path().append("/reference/")

	def examples_path(self):
		if not self.arduino_path():
			return None
		return self.arduino_path().append("/examples/")

	def sketches_path(self):
		## TODO - use prefs
		#print "path/sketchbooks_path", self.value("path/sketchbooks_path")
		return self.value("path/sketchbooks_path")
		#return QtCore.QString(config.SKETCHBOOKS_PATH)


	#def keywords_path(self):
		#return self.app_path().append("/keywords")

	def api_define_path(self):
		return self.app_path().append("/etc/api_define")

	def all_paths(self):
		ret = []
		ret.append(['Arduino', self.arduino_path()])
		ret.append(['arduino-pyqt', self.app_path()])
		ret.append(['Arduino svn/trunk', self.arduino_svn_path()])
		ret.append(['Help', self.help_path()])
		ret.append(['Examples', self.examples_path()])
		ret.append(['Sketchbooks', self.sketchbooks_path()])
		ret.append(['Hardware', self.hardware_path()])
		ret.append(['API', self.api_def_path()])
		return ret