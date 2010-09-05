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

#!/usr/bin/python

import commands
from PyQt4 import QtGui, QtCore
import os.path
import os
import time
from fileobject import FileObject
from synhigh import SyntaxHighlighter

class MainWindow (QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		
		# Set the window size when opened, title the window, and set the icon
		
		self.currentfile = FileObject(parent=self)

		self.resize(800,600)
		self.setWindowTitle('rIDE')
		self.setWindowIcon(QtGui.QIcon('icons/ride.png'))
		
		# Declare the text field widget, and make it the most important, because the Lady of the Lake raised aloft the blade Excalibur from the lake and gave it to the text widget. 
		
		self.textedit = QtGui.QTextEdit()
		self.setCentralWidget(self.textedit)
		self.textedit.setFontFamily("monospace")
		self.textedit.setLineWrapMode(0)
		self.textedit.setText('Welcome to rIDE\n\nPlease create a new file or open an existing one to be able to use rIDE.')
		self.textedit.setEnabled(False)
		self.connect(self.textedit, QtCore.SIGNAL('textChanged()'), self.whenchanged)

		self.highlighter = SyntaxHighlighter(self.currentfile)
		
		# Creates an exit button, sets its icon and adds functionality.
		
		exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
		exit.setShortcut('Ctrl+Q')
		exit.setStatusTip('Exit application')
		self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
		
		# Creates a similar shortcut for a new file
		
		newfile = QtGui.QAction(QtGui.QIcon('icons/newfile.png'), 'New', self)
		newfile.setShortcut('Ctrl+N')
		newfile.setStatusTip('Create a new file')
		self.connect(newfile, QtCore.SIGNAL('triggered()'), self.currentfile.newfile)
		
		# Creates a similar shortcut for opening a file
		
		openfile = QtGui.QAction(QtGui.QIcon('icons/openfile.png'), 'Open...', self)
		openfile.setShortcut('Ctrl+O')
		openfile.setStatusTip('Open a file')
		self.connect(openfile, QtCore.SIGNAL('triggered()'), self.currentfile.openfile)
		
		# Creates a similar shortcut for saving a file
				
		savefile = QtGui.QAction(QtGui.QIcon('icons/savefile.png'), 'Save...', self)
		savefile.setShortcut('Ctrl+S')
		savefile.setStatusTip('Create a new file')
		self.connect(savefile, QtCore.SIGNAL('triggered()'), self.currentfile.savefile)

		# Creates a similar shortcut for saving a file, forcing a dialog.
		
		saveas = QtGui.QAction(QtGui.QIcon('icons/savefile.png'), 'Save as...', self)
		saveas.setStatusTip('Save the project as a different filename')
		self.connect(saveas, QtCore.SIGNAL('triggered()'), self.currentfile.saveas)
		
		# Creates a similar shortcut for building a file
		
		buildonly = QtGui.QAction(QtGui.QIcon('icons/buildonly.png'), 'Build (Ctrl-T)', self)
		buildonly.setShortcut('Ctrl+T')
		buildonly.setStatusTip('Build the project')
		self.connect(buildonly, QtCore.SIGNAL('triggered()'), self.onlybuild)
		
		# Creates the build-and-run shortcut
		
		buildrun = QtGui.QAction(QtGui.QIcon('icons/buildandrun.png'), 'Build and Run (Ctrl-B)', self)
		buildrun.setShortcut('Ctrl+B')
		buildrun.setStatusTip('Build the project and run it')
		self.connect(buildrun, QtCore.SIGNAL('triggered()'), self.buildandrun)
		
		# Creates the run shortcut
		
		runonly = QtGui.QAction(QtGui.QIcon('icons/runonly.png'), 'Run (Ctrl-R)', self)
		runonly.setShortcut('Ctrl+R')
		runonly.setStatusTip('Run the latest build')
		self.connect(runonly, QtCore.SIGNAL('triggered()'), self.onlyrun)

		# Creates the copy shortcut
		
		copy = QtGui.QAction('Copy', self)
		copy.setShortcut('Ctrl+C')
		copy.setStatusTip('Copy the selected text')
		self.connect(copy, QtCore.SIGNAL('triggered()'), self.textedit, QtCore.SLOT('copy()'))

		# Create the cut shortcut
		
		cut = QtGui.QAction('Cut', self)
		cut.setShortcut('Ctrl+X')
		cut.setStatusTip('Cut the selected text')
		self.connect(cut, QtCore.SIGNAL('triggered()'), self.textedit, QtCore.SLOT('cut()'))
		
		paste = QtGui.QAction('Paste', self)
		paste.setShortcut('Ctrl+V')
		paste.setStatusTip('Paste text from the clipboard')
		self.connect(paste, QtCore.SIGNAL('triggered()'), self.textedit, QtCore.SLOT('paste()'))

		# Initialize Status bar
		
		statusbar = self.statusBar()
		self.langlabel = QtGui.QLabel()
		statusbar.addWidget(self.langlabel)
		
		# Creates the menu bar and the file menu, adding in the appropriate actions
		
		menubar = self.menuBar()
		file = menubar.addMenu('&File')
		file.addAction(newfile)
		file.addAction(openfile)
		file.addAction(savefile)
		file.addAction(saveas)
		file.addAction(exit)
		
		# Creates the edit menu, adding in the appropriate contents
		
		edit = menubar.addMenu('&Edit')
		edit.addAction(copy)
		edit.addAction(cut)
		edit.addAction(paste)
		
		# Make a toolbar with all the trimmings
		
		self.toolbar = self.addToolBar('Buttons')
		self.toolbar.addAction(newfile)
		self.toolbar.addAction(openfile)
		self.toolbar.addAction(savefile)
		self.toolbar.addAction(buildonly)
		self.toolbar.addAction(buildrun)
		self.toolbar.addAction(runonly)
		self.toolbar.addAction(exit)

	def onlybuild(self):
		# Ask if they want to save the file, then do so--otherwise, throw an error and tell them they want "onlyrun"--then save the file, build it with the appropriate command, and display the results.
		saved = True
		if os.path.isfile(self.currentfile.filename):
			test = open(self.currentfile.filename)
			if test.read() != self.textedit.toPlainText():
				saved = False
		else:
			saved = False
		if not saved:
			needsave = QtGui.QMessageBox.question(self, "WARNING: Save the file!", "You should save the file before continuing!", "OK", "Cancel")
			if needsave == 0:
				self.currentfile.savefile(True)

		if self.currentfile.language not in ["C++"]:
			QtGui.QMessageBox.about(self, "Build results", "This language doesn't need to be built first! Just hit 'Run'!")
			raise Exception("This is an interpreted language...")
		statz, outz = commands.getstatusoutput(self.currentfile.buildcomm)
		if statz != 0:
			os.system("xterm -e '" + self.currentfile.buildcomm + "; python pause.py'")
		else:
			QtGui.QMessageBox.about(self, "Build results", "The build succeeded!")

	def buildandrun(self):
		# Ask if they want to save the file, then do so--otherwise, throw an error--then save the file, build it with the appropriate command, and display the results.
		# If the command used to build it exits with an error, we have a problem--make sure it doesn't close to allow review of the errors, but don't try to run the binary.
		# If it makes it through, close the build window and run the program.
		if self.currentfile.language == "C++":
			self.onlybuild()
		self.onlyrun()

	def onlyrun(self):
		# Find the binary created by the IDE. If it doesn't exist, throw an error. Then, run it.
		if self.currentfile.language not in ['C++']:
			saved = True
			if os.path.isfile(self.currentfile.filename):
				test = open(self.currentfile.filename)
				if test.read() != self.textedit.toPlainText():
					saved = False
			else:
				saved = False
			if not saved:
				needsave = QtGui.QMessageBox.question(self, "WARNING: Save the file!", "You should save the file before continuing!", "OK", "Cancel")
				if needsave == 0:
					self.currentfile.savefile(True)
		os.system("xterm -e '" + self.currentfile.runcomm + "; python pause.py'")

	def whenchanged(self):
		self.textedit.setFontFamily("monospace")
		self.currentfile.saved = False
