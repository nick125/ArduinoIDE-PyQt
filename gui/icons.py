# -*- coding: utf-8 -*-
import os
from PyQt4 import QtGui

class Icon(QtGui.QIcon):

	def __init__(self, file_name):
		## TODO - this is assumed that the icons are placed. Its python dependant
		img_dir = os.path.dirname(__file__) + '../../images/icons/'
		full_path = img_dir + file_name
		QtGui.QIcon.__init__(self, full_path)



class Ico:
	Arduino = 'arduino.png'

	## sketch Related
	Sketch = 'page.png'
	Compile = 'arrow_in.png'
	Upload = 'arrow_join.png'


	## Help
	HelpDoc = 'page_white.png'

	## Directories
	Folder = 'folder.png'


	
	