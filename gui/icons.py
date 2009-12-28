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

	BootLoaderBurn = 'transmit_go.png'
	BootLoaders = 'transmit_blue.png'
	BootLoader = 'transmit.png'

	Board = 'brick.png'
	Boards = 'bricks.png'

	## sketch Related
	Sketches = 'book_open.png'
	Sketch = 'page.png'


	Upload = 'arrow_join.png'

	Compile = 'arrow_in.png'
	CompileError = 'exclamation.png'
	CompileOk = 'accept.png'

	## Help
	Help = 'help.png'
	HelpDoc = 'page_white.png'
	
	## Directories
	FileSystemBrowser = 'chart_organisation.png'
	Folder = 'folder.png'
	FolderAdd = 'folder_add.png'
	FolderEdit = 'folder_edit.png'
	FolderDelete = 'folder_delete.png'


	## widgets
	Add = 'add.png'
	Delete ='delete.png'
	Remove = 'delete.png'
	Cancel = 'bullet_black.png'
	Save = 'accept.png'
	Refresh = 'refresh.gif'

	Up = 'arrow_up.png'
	Down = 'arrow_down.png'

	Function = 'ruby.png'
	FunctionAdd = 'ruby_add.png'
	FunctionEdit = 'ruby.png'
	FunctionDelete = 'ruby_delete.png'
	FunctionReturn = 'bullet_go.png'
	FunctionParam = 'bullet_green.png'
	FunctionSub = 'bullet_red.png'

	Green = 'bullet_green.png'
	Blue = 'bullet_blue.png'
	Black = 'bullet_black.png'
	Yellow = 'bullet_yellow.png'
	#Black = 'bullet_black.png'
	
	

	WriteFile = 'book_next.png'

	Settings = 'cog.png'