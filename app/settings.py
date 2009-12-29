# -*- coding: utf-8 -*-
import os
import sys
from PyQt4 import QtCore, QtGui

class Settings(QtCore.QObject):

	date_format = "dd-MM-yyyy"
	date_time_format = "dd-MM-yyyy HH:mm"

	def __init__(self, main):
		QtCore.QObject.__init__(self, main)
		self.main = main
		self.qSettings = QtCore.QSettings("arduino-pyqt", "arduino-pyqt")

	def is_nix(self):
		return  'linux' in sys.platform # TODO use QT

	#################################################
	## Pass<>Thru for QSettings class
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


	#################################################
	## Window Save/Restore
	#################################################
	def save_window(self, windowName, window):
		self.qSettings.setValue( "window/%s/geometry" % windowName, QtCore.QVariant(window.saveGeometry()) )

	def restore_window(self, windowName, window):
		geo = self.qSettings.value( "window/%s/geometry" % windowName )
		window.restoreGeometry( geo.toByteArray() )


	#########################################################
	## Paths
	#########################################################
	def check_path(self, file_path):
		"""Checks file/path exists or return none"""
		d = QtCore.QFileInfo(file_path)
		if d.exists():
			return file_path
		return None

	def all_paths(self):
		"""Returns all paths as a dict - exlcuding superfilous"""
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

	## Arduino Path
	def arduino_path(self):
		return self.value("path/arduino_path")

	## Arduino SVN trunk
	def arduino_svn_path(self):
		return self.value("path/arduino_svn_path")

	## App Path - directory of parent dir
	def app_path(self):
		## TODO - user QT Object
		return  QtCore.QString(os.path.abspath( os.path.dirname(__file__)	+  '/../' ))

	## API Info Path - directory to yaml
	def api_define_path(self):
		## TODO - user QT Object
		return  self.app_path().append("/etc/api_define/")

	## Icons Dir
	def icons_path(self):
		return  self.app_path().append("/images/icons/")

	## Aarduino Hardware Dir
	def hardware_path(self, append_str=None):
		if not self.arduino_path():
			return None
		path = self.arduino_path().append("/hardware/")
		if append_str:
			return self.check_path(path.append(append_str))
		return self.check_path(path)

	## Help HTML files
	def help_path(self):
		if not self.arduino_path():
			return None
		return self.arduino_path().append("/reference/")

	## Exmaples Dir
	def examples_path(self):
		if not self.arduino_path():
			return None
		return self.arduino_path().append("/examples/")

	## Sketches Directory
	def sketches_path(self):
		return self.value("path/sketchbooks_path")

