#!/usr/bin/env python
# -*- coding: utf-8 -*-

# copyright: Peter Morgan <pedromorgan@gmail.com>
# License GPL

import sys
from PyQt4 import QtCore, QtGui

import gui.MainWindow

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)

	window = gui.MainWindow.MainWindow()
	window.show()

	sys.exit(app.exec_())

