# -*- coding: utf-8 -*-



class IPAdressWidget(QtGui.QWidget):

	
	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self, parent)

		self.main = main

		mainLayout = QtGui.QHBoxLayout(self)
		self.setLayout(mainLayout)

		self.lcds = []
		for i in [192, 168, 5, 10]:
			lcd  = QtGui.QLCDNumber(self)
			lcd.setNumDigits(3)
			lcd.display(i)
			mainLayout.addWidget(lcd)

	