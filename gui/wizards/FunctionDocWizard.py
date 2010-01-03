# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
#

##########################################################################
## Main Dialog
##########################################################################
class FunctionDocWizard(QtGui.QWizard):

	def __init__(self, parent):
		QtGui.QWizard.__init__(self, parent)

		self.history = []
		self.numPages = 0

		self.setWizardStyle( QtGui.QWizard.ModernStyle)
		self.setWindowTitle("Job Wizard")
		#self.setWindowIcon( dIcon(dIco.Wizzard) )
		self.setMinimumWidth( 400 )
		self.setMinimumHeight( 400 )


		self.addPage( CreateFunctionStart(self) )
		self.addPage( CreateParameterDescriptions(self) )


##########################################################################
## Create Function Page
##########################################################################
class CreateFunctionStart(QtGui.QWizardPage):

	def __init__(self, parent):
		QtGui.QWizardPage.__init__(self, parent)
		self.setTitle("Create Function")
		self.setSubTitle(" ") #Enter the name of the function to create")

		self.params = {}

		gridLayout = QtGui.QGridLayout()
		self.setLayout(gridLayout)

		## Help Label
		row = 0
		s = "Enter the same of the function<br>eg <font color=green>digitalRead</font> or <font color=green>Serial.write</font>"
		hlplbl = QtGui.QLabel(s)
		gridLayout.addWidget(hlplbl, row, 0, 1, 3)

		####################################
		##  Function Name
		row += 1
		hBox = QtGui.QHBoxLayout()
		gridLayout.addLayout(hBox, row, 0, 1, 3)
		#function_name = "foo"
		#lbl = QtGui.QLabel(function_name + "(")
		#lbl.setStyleSheet("font-weight: bold;")
	
		#hBox.addWidget(lbl)
		rx = QtCore.QRegExp()
		rx.setPattern("[aA-zZ][a-zA-Z0-9_]+");
		
		self.txtFunc = QtGui.QLineEdit(self)
		validator = QtGui.QRegExpValidator(rx, self.txtFunc)
		self.txtFunc.setValidator(validator)
		hBox.addWidget(self.txtFunc, 2)
		self.connect(self.txtFunc, QtCore.SIGNAL("textChanged (const QString&)"), self.on_set_function_text)

		self.lblFunc = QtGui.QLabel("()")
		self.lblFunc.setStyleSheet("font-weight: bold;")
		hBox.addWidget(self.lblFunc, 2)

		##########################
		## Single Permutation
		row += 1
		self.radioSingle = QtGui.QRadioButton("This function has only one permutation")
		self.radioSingle.setChecked(True)
		gridLayout.addWidget(self.radioSingle, row, 0, 1, 3)
		self.connect(self.radioSingle, QtCore.SIGNAL("clicked(bool)"), self.on_radio_permutation)

		##########################
		## Has Paramaters
		row += 1
		self.chkSingleHasArgs = QtGui.QGroupBox("This function has paramaters")
		self.chkSingleHasArgs.setDisabled(False)
		self.chkSingleHasArgs.setCheckable(True)
		self.chkSingleHasArgs.setChecked(False)
		gridLayout.addWidget(self.chkSingleHasArgs, row, 1, 1, 2)
		self.connect(self.chkSingleHasArgs, QtCore.SIGNAL("toggled(bool)"), self.on_single_has_params)
		gLay = QtGui.QVBoxLayout()
		self.chkSingleHasArgs.setLayout(gLay)
		##########################
		## txt Paramaeters
		# += 1
		s = "Enter the paramaters seperated by a comma,<br>"
		s += "eg <font color=green>pin, mode</font>"
		lbl = QtGui.QLabel(s)
		gLay.addWidget(lbl) #, row, 0, 1, 2)
		self.txtParameters = QtGui.QLineEdit("")
		if 1 == 0: # TODO
			rx = QtCore.QRegExp()
			rx.setPattern("[aA-zZ][a-zA-Z0-9_,]+")
			validator = QtGui.QRegExpValidator(rx, self.txtParameters)
			self.txtParameters.setValidator(validator)
		self.connect(self.txtParameters, QtCore.SIGNAL("textChanged (const QString&)"), self.on_set_function_text)
		gLay.addWidget(self.txtParameters)#, row, 2, 1, 1)

		###########################################################################
		## More than one Permutation
		###########################################################################
		row += 1
		self.radioMore = QtGui.QRadioButton("This function has more than one permutation")
		gridLayout.addWidget(self.radioMore, row, 0, 1, 3)
		self.connect(self.radioMore, QtCore.SIGNAL("clicked(bool)"), self.on_radio_permutation)

		row += 1
		self.groupManyParamaters = QtGui.QGroupBox("Parameters")
		self.groupManyParamaters.setDisabled(True)
		gridLayout.addWidget(self.groupManyParamaters, row, 1, 1, 2)
		#self.connect(self.chkSingleHasArgs, QtCore.SIGNAL("toggled(bool)"), self.on_single_has_params)
		gLay = QtGui.QVBoxLayout()
		self.groupManyParamaters.setLayout(gLay)
		##########################
		## txt Paramaeters
		# += 1
		s = "Enter the different paramater combinations<br>one per line.<br>Leave a blank line for no paramaters <br>eg<br>"
		s += "<font color=green><br>b, DEC<br>b, HEX<br>str, len</font>"

		lbl = QtGui.QLabel(s)
		gLay.addWidget(lbl) #, row, 0, 1, 2)#
		txt = "\nd, DEC,\n n, HEX\n str,   len,\n str,  ,    len,,    max,\n str, foo, bar, bing,  \n"
		self.txtManyParameters = QtGui.QPlainTextEdit(txt)
		self.connect(self.txtManyParameters, QtCore.SIGNAL("textChanged()"), self.on_set_function_text)
		gLay.addWidget(self.txtManyParameters)#, row, 2, 1, 1)

		###########################################################################
		## Preview Tree
		###########################################################################
		self.txtSyntax = QtGui.QTextEdit(self)
		gridLayout.addWidget(self.txtSyntax, 0, 3, 5, 1)


		###########################
		gridLayout.setColumnStretch(0, 1)
		gridLayout.setColumnStretch(1, 1)
		gridLayout.setColumnStretch(2, 4)

	def on_set_function_text(self, string=None):
		funk_name = "<font color=green>" + str(self.txtFunc.text()) + "</font>"
		if self.radioSingle.isChecked():
			funky_label = funk_name + "("
			if self.chkSingleHasArgs.isChecked():
				funky_label += "<font color=blue>" + str(self.txtParameters.text()) + "</font>"
			funky_label += ")"
			self.txtSyntax.setText(funky_label)
		else:
			#funky_label = "" #funk_name + "("<font color=blue>?</font> )"
			param_string = str(self.txtManyParameters.toPlainText())
			#lines = param_string.split("\n")
			funk_list = []
			for line in param_string.split("\n"):
				params_split = line.split(",") 
				funk_string = funk_name + "("
				param_list = []
				for param in line.split(","): 
					p = param.strip()
					if p != '':
						#print "param=", param
						param_list.append("<font color=blue>" + param + "</font>")
				funk_string += ", ".join(param_list)
				funk_string += ")"
				#'print funk_string
				if not funk_string in funk_list:
					funk_list.append(funk_string)
			funky_label = "<br>".join(funk_list)
			self.txtSyntax.setText(funky_label)
		#self.lblFunc.setText(funky_label)
		
		#self.set_tree_items()
	
	def on_single_has_params(self):
		print "ere",self.chkSingleHasArgs.isChecked()
		if self.chkSingleHasArgs.isChecked():
			self.txtParameters.setFocus()

	def on_radio_permutation(self):
		single_mode =  self.radioSingle.isChecked()
		#self.group
		self.groupManyParamaters.setDisabled(single_mode)
		
		self.on_set_function_text()

		if single_mode == False:
			self.txtManyParameters.setFocus()
		



##########################################################################
## Create Function Page 2
##########################################################################
class CreateParameterDescriptions(QtGui.QWizardPage):

	def __init__(self, parent):
		QtGui.QWizardPage.__init__(self, parent)
		self.setTitle("Parameter Descriptions Function")
		self.setSubTitle(" ") #Enter the name of the function to create")


		gridLayout = QtGui.QGridLayout()
		self.setLayout(gridLayout)
