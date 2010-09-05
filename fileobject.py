"""
Copyright 2010 Mark Holmquist and Logan May. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY MARK HOLMQUIST AND LOGAN MAY ``AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL MARK HOLMQUIST OR LOGAN
MAY OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the
authors and should not be interpreted as representing official policies, either expressed
or implied, of Mark Holmquist and Logan May.
"""

import os.path
import os
from PyQt4 import QtGui, QtCore
from synhigh import SyntaxHighlighter

class FileObject (object):

	def __init__(self, parent=None):
		self.parent = parent
		self.filename = ""
		self.language = ""
		self.runcomm = ""
		self.buildcomm = ""

	def newfile(self):
		languages = ["C++", "Python","Prolog", "Lisp", "Whitespace", "LOLCODE"]
		self.language, ok = QtGui.QInputDialog.getItem(self.parent, 'Choose a Language', 'Which language are you using today?', languages, 0, False)
		if ok:
			langlabel = "Current Language: " + self.language
			self.parent.textedit.clear()
			self.parent.textedit.setEnabled(True)
			self.parent.langlabel.setText("Current Language: " + self.language)
			self.runcomm = ""
			self.parent.highlighter = SyntaxHighlighter(self)

	def openfile(self):
		self.filename = QtGui.QFileDialog.getOpenFileName(self.parent, 'Open file...', os.path.expanduser('~'))
		if self.filename == "":
			return
		fileobject = open(self.filename, 'r')
		self.parent.textedit.setText(fileobject.read())
		self.findtype(self.filename.split(".")[-1])
		fileobject.close()
		self.parent.textedit.setEnabled(True)
		self.parent.langlabel.setText("Current Language: " + self.language)
		self.parent.highlighter = SyntaxHighlighter(self)
		self.parent.textedit.selectAll()
		self.parent.textedit.cut()
		self.parent.textedit.paste()

	def savefile(self, forcedia = False):
		# Take all the text in the editor, put all the text into a file, and change the filename to that.
		if self.filename == "" or forcedia:
			savedia = QtGui.QFileDialog()
			self.filename = savedia.getSaveFileName(self.parent, 'Save file...', os.path.expanduser('~'))
			savedia.close()
		if self.filename == "":
			return
		fileout = open(self.filename, 'w')
		fileout.write(self.parent.textedit.toPlainText())
		fileout.close()
		self.findtype(self.filename.split(".")[-1])

	def saveas(self):
		self.savefile(True)

	def findtype(self, ext):
		if ext == "cpp":
			self.language = "C++"
			self.runcomm = str(self.filename[:-4])
			self.buildcomm = "g++ " + str(self.filename) + " -o " + str(self.filename[:-4])

		elif ext == "py":
			self.language = "Python"
			self.runcomm = "python " + str(self.filename)
			self.buildcomm = ""

		elif ext == "pro":
			self.language = "Prolog"
			self.runcomm = "prolog -s " + str(self.filename)
			self.buildcomm = ""

		elif ext == "lisp":
			self.language = "Lisp"
			self.runcomm = "clisp " + str(self.filename)
			self.buildcomm = ""

		elif ext == "ws":
			self.language = "Whitespace"
			self.runcomm = "python whitespace/interpret.py " + str(self.filename)
			self.buildcomm = ""

		elif ext == "LOL":
			self.language = "LOLCODE"
			self.runcomm = "python lol.py -r " + str(self.filename)
			self.buildcomm = ""
	
