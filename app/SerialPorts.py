# -*- coding: utf-8 -*-
from PyQt4 import QtCore


""" 
	Most of this stuff is lifted from the pyserial scan* examples
"""

import serial
import glob



class SerialPorts(QtCore.QObject):

	def __init__(self, parent):
		QtCore.QObject.__init__(self, parent)


	def index(self):
		return glob.glob('/dev/ttyS*') + glob.glob('/dev/ttyUSB*')

"""
this return //y* NOT usb/*
def scan():
    #scan for available ports. return a list of tuples (num, name)
    available = []
    for i in range(256):
        try:
            s = serial.Serial(i)
            available.append( (i, s.portstr))
            s.close()   # explicit close 'cause of delayed GC in java
        except serial.SerialException:
            pass
    return available

if __name__=='__main__':
    print "Found ports:"
    for n,s in scan():
        print "(%d) %s" % (n,s)

"""