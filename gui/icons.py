# -*- coding: utf-8 -*-
import os
from PyQt4 import QtGui
from app.settings import settings

class Icon(QtGui.QIcon):
	"""
		An Icon helper
	"""
	def __init__(self, file_name):
		QtGui.QIcon.__init__(self, settings.icons_path().absoluteFilePath(file_name))

# TODO: Banish this! (said nick)
# TODO: seems to work at the moment for pedro.. later maybe this would be ina resource file ?


class Icons:

	Arduino = 'arduino.png'

	BootLoaderBurn = 'transmit_go.png'
	BootLoaders = 'transmit_blue.png'
	BootLoader = 'transmit.png'

	Board = 'brick.png'
	Boards = 'bricks.png'

	## sketch Related
	Sketches = 'book_open.png'
	Sketch = 'page.png'


	## Compile related
	Upload = 'arrow_up.png'
	Compile = 'arrow_right.png'
	CompileUpload = 'arrow_merge.png'
	CompileError = 'exclamation.png'
	CompileOk = 'accept.png'

	## Directories
	FileSystemBrowser = 'chart_organisation.png'
	Folder = 'folder.png'
	FolderAdd = 'folder_add.png'
	FolderEdit = 'folder_edit.png'
	FolderDelete = 'folder_delete.png'

	## General
	Add = 'add.png'
	Delete = 'delete.png'
	Remove = 'delete.png'
	Cancel = 'bullet_black.png'
	Save = 'accept.png'
	Refresh = 'refresh.gif'

	Up = 'arrow_up.png'
	Down = 'arrow_down.png'

	Green = 'bullet_green.png'
	Blue = 'bullet_blue.png'
	Black = 'bullet_black.png'
	Yellow = 'bullet_yellow.png'
	Pink = 'bullet_ping.png'

	# Api and help
	Functions = 'ruby.png'
	Function = 'ruby.png'
	FunctionAdd = 'ruby_add.png'
	FunctionEdit = 'ruby.png'
	FunctionDelete = 'ruby_delete.png'
	FunctionReturn = 'bullet_go.png'
	FunctionParam = 'bullet_green.png'
	FunctionSub = 'bullet_red.png'

	Keyword = 'page_white.png'
	Help = 'help.png'
	HelpDoc = 'page_white.png'
	Html = 'page_white.png'



	
	

	WriteFile = 'book_next.png'

	Settings = 'cog.png'
	Exit  = 'delete.png'
# XX: Remove this hack once Ico is out of use
Ico = Icons
