# -*- coding: utf-8 -*-
"""
	The Signal Dispatcher
"""

from PyQt4 import QtCore

class Dispatcher(QtCore.QObject):
	"""
		Implements a signal dispatcher
	"""
	def __init__(self):
		"""
			Initializes the dispatcher
		"""
		QtCore.QObject.__init__(self)

	def __getattr__(self, name):
		"""
			Handles the magic class stuff!
		"""
		def emitter(*args):
			"""
				Returned from the __getattr__ call
			"""
			if len(args) == 0:
				self.emit(QtCore.SIGNAL("%s()" % name))
				print "emitting %s()" % name
			else:
				self.emit(QtCore.SIGNAL(name), *args)
				print "emitting %s with args"
		return emitter

dispatcher = Dispatcher()

class Test:
	@QtCore.pyqtSlot()
	def test():
		print "test from the handler!"
	QtCore.QObject.connect(dispatcher, QtCore.SIGNAL("test()"), test)
