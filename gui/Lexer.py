# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
from PyQt4.Qsci import QsciScintilla, QsciLexerCPP, QsciLexerCustom

#########################################################################
## Lexer
#########################################################################

class ArduinoLexer(QsciLexerCPP):

	def __init__(self, parent):
		QsciLexerCPP.__init__(self, parent)
		font = self.defaultFont()
		

class DEADArduinoLexer(QsciLexerCustom):
	def __init__(self, parent):
		QsciLexerCustom.__init__(self, parent)
		self._styles = {
			0: 'Default',
			1: 'Comment_Start',
			2: 'Comment',
			3: 'Comment_End'
			}
		for key,value in self._styles.iteritems():
			setattr(self, value, key)
		self._foldcompact = True

	def foldCompact(self):
		return self._foldcompact

	def setFoldCompact(self, enable):
		self._foldcompact = bool(enable)

	def language(self):
		return 'Config Files'

	def description(self, style):
		return self._styles.get(style, '')

	def defaultColor(self, style):
		if style == self.Default:
			return QtGui.QColor('#000000')
		elif style == self.Comment or style == self.Comment_End or style == self.Comment_Start:
			return QtGui.QColor('#A0A0A0')
		return QsciLexerCustom.defaultColor(self, style)

	def defaultFont(self, style):
		if style == self.Comment or self.Comment_End:
			if sys.platform in ('win32', 'cygwin'):
				return QtGui.QFont('Comic Sans MS', 9, QtGui.QFont.Bold)
			return QtGui.QFont('Bitstream Vera Serif', 9, QtGui.QFont.Normal)
		return QsciLexerCustom.defaultFont(self, style)

	def defaultPaper(self, style):
		# Here we change the color of the background.
		# We want that colorize all the background of the line.
		# This is done by using the following method defaultEolFill() .
		if style == self.Comment or style == self.Comment_End or style == self.Comment_Start:
			return QtGui.QColor('#FFEECC')
		return QsciLexerCustom.defaultPaper(self, style)

	def defaultEolFill(self, style):
		# This allowed to colorize all the background of a line.
		if style == self.Comment or style == self.Comment_End or style == self.Comment_Start:
			return True
		return QsciLexerCustom.defaultEolFill(self, style)

	def styleText(self, start, end):
		editor = self.editor()
		if editor is None:
			return

		SCI = editor.SendScintilla
		GETFOLDLEVEL = QsciScintilla.SCI_GETFOLDLEVEL
		SETFOLDLEVEL = QsciScintilla.SCI_SETFOLDLEVEL
		HEADERFLAG = QsciScintilla.SC_FOLDLEVELHEADERFLAG
		LEVELBASE = QsciScintilla.SC_FOLDLEVELBASE
		NUMBERMASK = QsciScintilla.SC_FOLDLEVELNUMBERMASK
		WHITEFLAG = QsciScintilla.SC_FOLDLEVELWHITEFLAG
		set_style = self.setStyling

		source = ''
		if end > editor.length():
			end = editor.length()
		if end > start:
			source = bytearray(end - start)
			SCI(QsciScintilla.SCI_GETTEXTRANGE, start, end, source)
		if not source:
			return

		compact = self.foldCompact()

		index = SCI(QsciScintilla.SCI_LINEFROMPOSITION, start)
		if index > 0:
			pos = SCI(QsciScintilla.SCI_GETLINEENDPOSITION, index - 1)
			state = SCI(QsciScintilla.SCI_GETSTYLEAT, pos)
		else:
			state = self.Default

		self.startStyling(start, 0x1f)

		for line in source.splitlines(True):
			# Try to uncomment the following line to see in the console
			# how Scintiallla works. You have to think in terms of isolated
			# lines rather than globally on the whole text.
			#print line

			length = len(line)
			# We must take care of empty lines.
			# This is done here.
			if length == 1:
				if state == self.Comment_End :
					state = self.Default
				elif state == self.Comment_Start:
					state = self.Comment
			else:
				if line.startswith('/*'):
					state = self.Comment_Start
				elif line.startswith('*/'):
					if state == self.Comment or state == self.Comment_Start:
						state = self.Comment_End
					else:
						state = self.Default
				elif state == self.Comment or state == self.Comment_Start:
					state = self.Comment
				else:              
					state = self.Default

			set_style(length, state)

			# Definition of the folding.
			if state == self.Comment_Start:
				print '-'*30
				print line
				level = LEVELBASE | HEADERFLAG
			elif state == self.Comment or state == self.Comment_End:
				level = LEVELBASE + 1
			elif state == self.Default:
				level = LEVELBASE

			SCI(SETFOLDLEVEL, index, level)

			index += 1
